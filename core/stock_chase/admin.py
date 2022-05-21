from django.contrib import admin
from stock_chase.models import ProdcutListing, ProductGroup


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('sales_channel', 'name', 'stock', 'stock_code', 'is_bundle', 'status')
    list_display_links = ('sales_channel', 'name',)
    search_fields = ['sales_channel', 'name', ]


admin.site.register(ProdcutListing, ProductsAdmin)


class BundleGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'group_code', 'bundle_product',)


admin.site.register(ProductGroup, BundleGroupAdmin)
