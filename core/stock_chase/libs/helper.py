
from django.contrib import messages

from django.db.models import Min

from stock_chase.models import ProdcutListing, ProductGroup


def create_bundle_group(bundle_products, group_name, group_code):
    try:
        bp_objects = ProdcutListing.objects.filter(id__in=bundle_products)

        for item in bp_objects:
            ProductGroup.objects.create(
                group_name=group_name,
                group_code=group_code,
                bundle_product=item
            )
    except Exception as err:
        pass


def create_new_product(sales_channel, name, stock, stock_code, is_bundle, status):
    try:
        new_product = ProdcutListing.objects.create(
            sales_channel=sales_channel,
            name=name,
            stock=stock,
            stock_code=stock_code,
            is_bundle=is_bundle,
            status=status,
        )
        return new_product
    except Exception as err:
        pass


def has_previous_stock_code(request, stock_code, group_code=None):
    try:
        p_list = ProdcutListing.objects.filter(stock_code=stock_code)
        bp_list = ProductGroup.objects.filter(group_code=group_code)
        if len(p_list) >= 1 or len(bp_list) >= 1:
            messages.error(request,
                           'Stock code or group code previously defined to another product, please define again!')
            return True

    except:
        pass
    return False


def exceed_acceptable_stock(request, stock, bundle_products):
    max_available_stock = ProdcutListing.objects.filter(id__in=bundle_products).aggregate(Min('stock'))
    max_value = max_available_stock['stock__min']
    if int(stock) >= max_value:
        return max_value




def exceed_maximum_stock(request, stock, product_id):
    group_code = ProductGroup.objects.get(bundle_product_id=product_id).group_code
    min_available_stock = ProductGroup.objects.select_related('bundle_product').filter(group_code=group_code) \
        .exclude(bundle_product_id=product_id).aggregate(Min('bundle_product__stock'))
    min_value = min_available_stock['bundle_product__stock__min']
    if int(stock) <= min_value:
        return False
    messages.error(request, f'Stock amount must not exceed {min_value}')
    return True
