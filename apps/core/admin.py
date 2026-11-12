import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from .models import Lead, SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Brand & Contact",
            {
                "fields": (
                    "company_name",
                    "logo",
                    "phone",
                    "whatsapp_number",
                    "email",
                    "address",
                    "gst_number",
                    "msme_number",
                    "catalog_pdf",
                    "linkedin_url",
                    "instagram_url",
                    "youtube_url",
                    "facebook_url",
                )
            },
        ),
        (
            "Home Page Hero",
            {
                "fields": (
                    "hero_tagline",
                    "hero_title",
                    "hero_title_highlight",
                    "hero_subtitle",
                    "hero_image",
                )
            },
        ),
        (
            "Ads & Alerts",
            {"fields": ("google_tag_id", "meta_pixel_id", "lead_notify_email")},
        ),
    )

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.action(description="Export selected leads to CSV")
def export_leads_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="leads.csv"'
    response.write("﻿")  # BOM so Excel opens UTF-8 correctly
    writer = csv.writer(response)
    writer.writerow(
        [
            "Date",
            "Type",
            "Name",
            "Company",
            "Phone",
            "Email",
            "City",
            "Product",
            "Quantity",
            "Message",
            "Source Page",
            "UTM Source",
            "UTM Medium",
            "UTM Campaign",
            "Status",
        ]
    )
    for lead in queryset:
        writer.writerow(
            [
                timezone.localtime(lead.created_at).strftime("%Y-%m-%d %H:%M"),
                lead.get_inquiry_type_display(),
                lead.full_name,
                lead.company_name,
                lead.phone,
                lead.email,
                lead.city,
                lead.product_interest,
                lead.quantity,
                lead.message,
                lead.source_page,
                lead.utm_source,
                lead.utm_medium,
                lead.utm_campaign,
                lead.get_status_display(),
            ]
        )
    return response


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "email",
        "message",
        "product_interest",
        "created_at",
        "company_name",
        "inquiry_type",
        "utm_source",
        "status",
    )
    ordering = ("-created_at",)
    list_filter = ("status", "inquiry_type", "utm_source", "created_at")
    list_editable = ("status",)
    search_fields = ("full_name", "phone", "company_name", "city", "email")
    readonly_fields = (
        "source_page",
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "created_at",
    )
    date_hierarchy = "created_at"
    actions = [export_leads_to_csv]

    def has_add_permission(self, request):
        return False  # leads only come from the website
