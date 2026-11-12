from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related("category")
    active_category = request.GET.get("category", "")
    if active_category:
        products = products.filter(category__slug=active_category)
    return render(
        request,
        "catalog/product_list.html",
        {
            "categories": Category.objects.all(),
            "products": products,
            "active_category": active_category,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related("images", "specs"),
        slug=slug,
        is_active=True,
    )
    return render(request, "catalog/product_detail.html", {"product": product})
