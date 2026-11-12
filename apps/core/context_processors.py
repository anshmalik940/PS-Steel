from apps.catalog.models import Product

from .models import SiteSetting


def site(request):
    """Makes `site` and `footer_products` available in every template."""
    return {
        "site": SiteSetting.load(),
        "footer_products": Product.objects.filter(is_active=True)[:6],
    }
