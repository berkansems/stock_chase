from django import forms
from stock_chase.models import ProdcutListing, ProductGroup


class ProductsAddingForm(forms.ModelForm):
    class Meta:
        model = ProdcutListing
        fields = '__all__'
        exclude = ('is_bundle', 'stock',)


class ProductsGroupAddingForm(forms.ModelForm):
    class Meta:
        model = ProductGroup
        fields = '__all__'
        exclude = ('bundle_product',)
