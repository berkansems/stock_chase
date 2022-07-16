'''here is all methods of project'''
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from stock_chase.forms import ProductsAddingForm, ProductsGroupAddingForm
from stock_chase.libs.helper import has_previous_stock_code, exceed_acceptable_stock, \
    create_new_product, create_bundle_group, exceed_maximum_stock
from stock_chase.models import ProdcutListing, ProductGroup
from django.db.models import Min


def home(request):
    '''home page method'''
    product_count = ProdcutListing.objects.count()
    context = {'product_count': product_count}
    return render(request, 'panel.html', context=context)


def add_product(request):
    '''method for adding new product'''
    product_list = ProdcutListing.objects.exclude(is_bundle=True)\
        .values('id', 'name', 'sales_channel')
    if request.method == 'POST':
        sales_channel = request.POST.get('sales_channel')
        name = request.POST.get('name')
        stock = request.POST.get('stock')
        stock_code = request.POST.get('stock_code')
        is_bundle = True if request.POST.get('is_bundle') == 'on' else False
        status = True if request.POST.get('status') == 'on' else False
        group_name = request.POST.get('group_name')
        group_code = request.POST.get('group_code')
        bundle_products = request.POST.getlist('bundle_products')
        max_accept = None
        if is_bundle:
            if has_previous_stock_code(request, stock_code, group_code) is True:
                return redirect('add_product')
            max_accept = exceed_acceptable_stock(request, stock, bundle_products)
        amount = max_accept if max_accept is not None else stock
        new_product = create_new_product(sales_channel, name, amount, stock_code, is_bundle, status)
        bundle_products.append(new_product.id)

        if is_bundle:
            create_bundle_group(bundle_products, group_name, group_code)

        return redirect('list_products')

    context = {"product_list": product_list}
    return render(request, 'product_add.html', context)


def list_products(request):
    '''method for listing products'''
    products = ProdcutListing.objects.all().order_by('sales_channel')
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        products = paginator.page(1)

    product_count = len(products)
    context = {'product_count': product_count, 'products': products}
    return render(request, 'product_list.html', context=context)


def toggle_product(request, pk):
    '''method for changing products status'''
    product = ProdcutListing.objects.get(id=pk)
    product.status = product.statusChange
    product.save()
    messages.success(request, 'Product status changed successfully')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_product(request, pk):
    '''method for deleting products and related bundle products'''

    product = ProdcutListing.objects.get(id=pk)
    product_groups = ProductGroup.objects.filter(bundle_product_id=pk).values('group_code')
    if len(product_groups) >= 1:
        related_groups = ProductGroup.objects.filter(group_code__in=product_groups)
        related_bundle_products = ProductGroup.objects.filter(group_code__in=product_groups) \
            .select_related('bundle_product').distinct() \
            .values('bundle_product__id', 'bundle_product__is_bundle')
        # find related bundle_products which contains the product
        product_to_delete = []
        for item in related_bundle_products:
            if item['bundle_product__is_bundle']:
                product_to_delete.append(item['bundle_product__id'])
        # delete related bundle_products
        related_groups.delete()
        ProdcutListing.objects.filter(id__in=product_to_delete).delete()

    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('list_products')


def edit_product(request, pk):
    '''method to edite products '''
    context = {'id': pk}
    try:
        product = ProdcutListing.objects.get(id=pk)
        form = ProductsAddingForm(instance=product)
        if request.method == "POST":
            form = ProductsAddingForm(request.POST, instance=product)

            if form.is_valid():
                form.save()
                messages.success(request, 'Saved Successfully!')
            else:
                messages.error(request, 'Form is not valid!')
            return redirect('list_products')

        context.update({"form": form})
    except Exception as err:
        messages.error(request, err)
    return render(request, 'product_update.html', context)


def edit_product_group(request, pk):
    '''method to edite bundled product '''
    context = {}
    try:
        product_group = ProductGroup.objects.get(bundle_product_id=pk)
        related_groups = ProductGroup.objects.filter(group_code=product_group.group_code)

        form = ProductsGroupAddingForm(instance=product_group)
        if request.method == "POST":
            form = ProductsGroupAddingForm(request.POST, instance=product_group)

            if form.is_valid():
                form.save()
                for item in related_groups:
                    item.group_code = form.cleaned_data.get('group_code')
                    item.group_name = form.cleaned_data.get('group_name')
                    item.save()
                messages.success(request, 'Saved Successfully!')
            else:
                messages.error(request, 'Form is not valid!')
            return redirect('list_products')

        context.update({"form": form})
    except Exception as err:
        messages.error(request, err)
    return render(request, 'product_group_update.html', context=context)


def trade_now(request):
    '''sale logic run here'''
    products = ProdcutListing.objects.all().order_by('sales_channel')
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        amount = int(request.POST.get('amount')) if request.POST.get('amount') != '' else None
        product = ProdcutListing.objects.get(id=product_id)
        if amount is None:
            messages.error(request, 'Please select purchase amount!')
            return redirect('trade_now')
        elif amount > product.stock:
            messages.error(request, f'Maximum purchase amount is {product.stock}!')
            return redirect('trade_now')
        reduce_stock(request, product_id)

    context = {'products': products}
    return render(request, 'trade_now.html', context=context)


def increase_stock(request, pk):
    '''increase stock amount'''
    product = ProdcutListing.objects.get(id=pk)
    product.stock += 1
    if product.is_bundle:
        if exceed_maximum_stock(request, stock=product.stock, product_id=product.id) is True:
            return redirect('list_products')

    product.status = True
    product.save()
    group_code = ProductGroup.objects.get(bundle_product_id=pk).group_code
    min_available_stock = ProductGroup.objects.select_related('bundle_product').filter(group_code=group_code) \
        .exclude(bundle_product__is_bundle=True).aggregate(Min('bundle_product__stock'))

    minimum = int(min_available_stock['bundle_product__stock__min'])
    print(minimum)
    related_bundle = ProductGroup.objects.select_related('bundle_product') \
        .filter(group_code=group_code, bundle_product__is_bundle=True).values('bundle_product_id')

    _list = []
    for item in related_bundle:
        _list.append(int(item['bundle_product_id']))
    print(_list)
    bundle_products_list = ProdcutListing.objects.filter(id__in=_list)
    for product in bundle_products_list:
        product.stock = minimum
        product.save()

    return redirect('list_products')


def calculate_bundle_stocks(product, new_amount):
    '''reduce bundle product stock amount'''
    if product.is_bundle is False:
        product_group_list = ProductGroup.objects.filter(bundle_product_id=product.id).values('group_code')
        if len(product_group_list) > 0:
            group_list = []
            for item in product_group_list:
                group_list.append(item['group_code'])

            bundle_products = ProductGroup.objects.select_related('bundle_product') \
                .filter(group_code__in=group_list, bundle_product__is_bundle=True) \
                .exclude(bundle_product_id=product.id).values('bundle_product__id', 'bundle_product__stock')

            if len(bundle_products) > 0:
                for item in bundle_products:
                    if item['bundle_product__stock'] > new_amount:
                        bunlde_product = ProdcutListing.objects.get(id=item['bundle_product__id'])
                        bunlde_product.stock = new_amount
                        bunlde_product.save()


def reduce_stock(request, pk):
    '''reduce stock amount if just_bundle it will only change bundle products stock amount'''

    product = ProdcutListing.objects.get(id=pk)
    try:
        amount = int(request.POST.get('amount'))
    except:
        amount = 1

    if product.stock >= 1:
        if product.is_bundle:
            product.stock = product.stock - amount
            product.save()
        else:
            candidate_reduce_stock_products = ProdcutListing.objects.filter(
                stock_code=product.stock_code, is_bundle=False)
            for product in candidate_reduce_stock_products:
                product.stock -= amount
                product.save()
                # if (product.stock - amount)>0:
                #     product.stock = product.stock - amount
                # else:
                #     product.stock = 0
                # product.save()
                # calculate_bundle_stocks(product, product.stock )

    return redirect('list_products')
