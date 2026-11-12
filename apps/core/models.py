from django.db import models


class SiteSetting(models.Model):
    """Everything the client can edit about the site itself. Single row only."""

    # Brand & contact
    company_name = models.CharField(max_length=100, default="PS Kalash Steel")
    logo = models.ImageField(upload_to="site/", blank=True)
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(
        max_length=15, help_text="Digits only with country code, e.g. 919876543210"
    )
    email = models.EmailField()
    address = models.TextField()
    gst_number = models.CharField(max_length=20, blank=True, verbose_name="GST Number")
    msme_number = models.CharField(max_length=20, blank=True, verbose_name="MSME Number")

    catalog_pdf = models.FileField(
        upload_to="brochures/", blank=True, verbose_name="Catalogue PDF"
    )
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)


    # Home hero
    hero_tagline = models.CharField(
        max_length=100, default="Everyday Essentials in Stainless Steel"
    )
    hero_title = models.CharField(max_length=100, default="Stronger Houseware")
    hero_title_highlight = models.CharField(
        max_length=100,
        default="For a Brighter Tomorrow",
        help_text="Shown in the copper colour after the title",
    )
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="site/", blank=True)

    # Ads & alerts
    google_tag_id = models.CharField(
        max_length=30, blank=True, help_text="G-XXXXXXX or AW-XXXXXXX"
    )
    meta_pixel_id = models.CharField(max_length=30, blank=True)
    lead_notify_email = models.EmailField(
        blank=True, help_text="New inquiry alerts are sent to this address"
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # only one row ever
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]


class Lead(models.Model):
    """Every inquiry from every form on the site."""

    TYPE_CHOICES = [
        ("bulk", "Bulk Order"),
        ("reseller", "Reseller / Distributor"),
        ("contact", "General"),
    ]
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("converted", "Converted"),
        ("junk", "Junk"),
    ]

    inquiry_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="bulk")
    full_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    product_interest = models.CharField(max_length=200, blank=True)
    quantity = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)

    # Ad attribution, filled automatically
    source_page = models.CharField(max_length=500, blank=True)
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Lead / Inquiry"
        verbose_name_plural = "Leads / Inquiries"
        indexes = [models.Index(fields=["-created_at"])]

    def __str__(self):
        return f"{self.full_name} ({self.phone})"
