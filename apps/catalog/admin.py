from django.contrib import admin

from .models import Category, Product, ProductImage, ProductSpec


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 3


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "is_active", "order")
    list_editable = ("is_featured", "is_active", "order")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductSpecInline, ProductImageInline]
    fieldsets = (
        (None, {"fields": ("category", "title", "slug")}),
        ("Content", {"fields": ("short_description", "description", "image")}),
        ("Display", {"fields": ("is_featured", "is_active", "order")}),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image", "order")
    list_filter = ("product",)
    search_fields = ("product__title",)


@admin.register(ProductSpec)
class ProductSpecAdmin(admin.ModelAdmin):
    list_display = ("product", "label", "value", "order")
    list_filter = ("product",)
    search_fields = ("product__title", "label", "value")
