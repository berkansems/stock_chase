'''here is a template library which is accessible in templates  '''
from django import template
from stock_chase.models import ProdcutListing
register = template.Library()


@register.simple_tag(takes_context=True)
def check_bundle_product(context, id):
    '''to check if product is bundle or not'''
    is_bundle = ProdcutListing.objects.get(id=id).is_bundle
    if is_bundle:
        context['is_bundle'] = True
    return ''
