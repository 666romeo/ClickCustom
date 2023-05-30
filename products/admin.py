from django.contrib import admin

from products.models import Product, ProductCategory

admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'description')
    fields = ('image', 'name', 'description', ('price', 'quantity'), 'category')
    search_fields = ('name',)
    ordering = ('name',)