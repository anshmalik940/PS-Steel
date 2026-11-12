from django.urls import path
from django.views.generic import TemplateView

from . import seo, views


def page(name):
    """A plain static page: no view logic needed."""
    return TemplateView.as_view(template_name=f"core/{name}.html")


urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", page("about"), name="about"),
    path("for-resellers/", page("resellers"), name="resellers"),
    path("contact/", page("contact"), name="contact"),
    path("inquiry/", views.submit_inquiry, name="submit_inquiry"),
    path("thank-you/", views.thank_you, name="thank_you"),
    path("privacy-policy/", page("privacy"), name="privacy"),
    path("terms/", page("terms"), name="terms"),
    path("robots.txt", seo.robots_txt, name="robots"),
    path("sitemap.xml", seo.sitemap_xml, name="sitemap"),
]
