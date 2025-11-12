from django.contrib import admin
from .models import Category, Brand, Perfume, Cart, CartItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'brand', 'category', 'price', 'stock_quantity', 'is_active']
    list_filter = ['brand', 'category', 'gender', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />'
        return "Sin imagen"
    image_preview.short_description = 'Vista Previa'
    image_preview.allow_tags = True

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'perfume', 'quantity']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['perfume', 'user', 'rating', 'created_at']
