from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

admin.site.register(Category)

admin.site.register(Supplier)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'low_stock_alert', 'category', 'supplier')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'sku')

    def low_stock_alert(self, obj):
        if obj.is_low_stock():
            return format_html('<span style = "color: red;">Low Stock: {}</span>', obj.quantity)
        return format_html('<span>{}</span>', obj.quantity)
    

    low_stock_alert.short_description = 'Stock Status'

admin.site.register(Product, ProductAdmin)


class StockLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_changed', 'date_changed', 'reason')
    list_filter = ('reason', 'date_changed')
    search_fields = ('product__name',)


    def save_model(self, request, obj, form, change):
        # Call the original save
        super().save_model(request, obj, form, change)

        # Update the product's stock based on the StockLog entry
        product = obj.product
        product.quantity += obj.quantity_changed
        product.save()  # Save the updated product stock
    
admin.site.register(StockLog, StockLogAdmin)
