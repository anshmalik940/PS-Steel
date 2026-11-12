"""robots.txt and sitemap.xml.

Deliberately hand-written rather than pulling in django.contrib.sitemaps:
this site has a handful of static pages plus the product list, so a plain
view is smaller and easier to follow.
"""
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from apps.catalog.models import Product

STATIC_PAGES = [
    ("home", "1.0", "monthly"),
    ("product_list", "0.9", "weekly"),
    ("resellers", "0.8", "monthly"),
    ("about", "0.6", "yearly"),
    ("contact", "0.6", "yearly"),
    ("privacy", "0.2", "yearly"),
    ("terms", "0.2", "yearly"),
]


def robots_txt(request):
    host = request.get_host()
    scheme = request.scheme
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /inquiry/",
        "Disallow: /thank-you/",   # keep the conversion page out of search results
        "",
        f"Sitemap: {scheme}://{host}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    base = f"{request.scheme}://{request.get_host()}"
    today = timezone.localdate().isoformat()

    urls = [
        (base + reverse(name), today, changefreq, priority)
        for name, priority, changefreq in STATIC_PAGES
    ]
    for product in Product.objects.filter(is_active=True):
        urls.append(
            (
                base + product.get_absolute_url(),
                product.created_at.date().isoformat(),
                "monthly",
                "0.8",
            )
        )

    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, changefreq, priority in urls:
        body.append(
            f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod>"
            f"<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>"
        )
    body.append("</urlset>")
    return HttpResponse("\n".join(body), content_type="application/xml")
