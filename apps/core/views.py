import logging

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.catalog.models import Product

from .forms import LeadForm
from .models import SiteSetting

logger = logging.getLogger(__name__)


def home(request):
    featured = Product.objects.filter(is_active=True, is_featured=True)
    return render(request, "core/home.html", {"featured_products": featured})


@require_POST
def submit_inquiry(request):
    """Single endpoint for every inquiry form on the site."""
    back = request.META.get("HTTP_REFERER", "/")
    if not url_has_allowed_host_and_scheme(back, allowed_hosts={request.get_host()}):
        back = "/"

    # Honeypot: a hidden field that only bots fill in.
    if request.POST.get("website"):
        return redirect("home")

    form = LeadForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please enter your name and a valid mobile number.")
        return redirect(back)

    lead = form.save(commit=False)
    lead.source_page = back[:500]
    for key, value in request.session.get("utm", {}).items():
        setattr(lead, key, value)
    lead.save()

    notify_sales(lead)
    request.session["lead_submitted"] = True
    return redirect("thank_you")


def thank_you(request):
    # Only fire the ad conversion when a form was actually just submitted,
    # so a refresh or a direct visit does not create a fake conversion.
    fire_conversion = request.session.pop("lead_submitted", False)
    return render(request, "core/thank_you.html", {"fire_conversion": fire_conversion})


def notify_sales(lead):
    site = SiteSetting.load()
    if not site.lead_notify_email:
        return
    body = "\n".join(
        [
            f"Type: {lead.get_inquiry_type_display()}",
            f"Name: {lead.full_name}",
            f"Company: {lead.company_name}",
            f"Phone: {lead.phone}",
            f"Email: {lead.email}",
            f"City: {lead.city}",
            f"Product: {lead.product_interest}",
            f"Quantity: {lead.quantity}",
            f"Message: {lead.message}",
            "",
            f"Page: {lead.source_page}",
            f"Campaign: {lead.utm_source} / {lead.utm_medium} / {lead.utm_campaign}",
        ]
    )
    try:
        send_mail(
            f"New lead: {lead.full_name} ({lead.phone})",
            body,
            None,
            [site.lead_notify_email],
            fail_silently=False,
        )
    except Exception:
        # The lead is already saved; never lose it because SMTP is down.
        logger.exception("Could not send lead alert email for lead %s", lead.pk)
