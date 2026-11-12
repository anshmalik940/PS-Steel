from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower number shows first")

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    short_description = models.CharField(
        max_length=255, help_text="One line. Also used as the SEO meta description."
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", help_text="Main product photo")
    is_featured = models.BooleanField(default=False, help_text="Show on the home page")
    is_active = models.BooleanField(
        default=True, help_text="Untick to hide from the site without deleting"
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower number shows first")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/gallery/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Gallery image"

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductSpec(models.Model):
    """One row of the specification table.

    Examples: Grade / SS 202, Sizes / 500 ml, 750 ml, MOQ / 100 pcs
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specs")
    label = models.CharField(max_length=60, help_text="e.g. Grade, Sizes, MOQ")
    value = models.CharField(max_length=255, help_text="e.g. SS 202")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Specification"

    def __str__(self):
        return f"{self.label}: {self.value}"
