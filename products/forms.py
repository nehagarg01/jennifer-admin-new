from decimal import Decimal

from django import forms
from django.utils.timezone import now, localtime

from core.forms import SearchForm
from .models import Product, ProductAttribute
from schedule.models import Schedule


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'body_html', 'handle', 'product_type', 'vendor',
                  'shopify_id', 'materials', 'styles', 'features']

    materials = forms.ModelMultipleChoiceField(
        queryset=ProductAttribute.objects.filter(attribute_type="MA"))
    styles = forms.ModelMultipleChoiceField(
        queryset=ProductAttribute.objects.filter(attribute_type="ST"))
    features = forms.ModelMultipleChoiceField(
        queryset=ProductAttribute.objects.filter(attribute_type="FT"),
        required=False)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['materials'].initial = self.instance.materials()
            self.fields['styles'].initial = self.instance.styles()
            self.fields['features'].initial = self.instance.features()


class ProductScheduleChangeForm(forms.Form):
    schedule = forms.ModelChoiceField(
        empty_label=None,
        queryset=Schedule.objects.filter(date__gt=localtime(now()).date()))


class ChangeForm(forms.Form):
    title = forms.CharField()
    compare_at_price = forms.DecimalField(decimal_places=2, min_value=Decimal('0.00'))
    price = forms.DecimalField(decimal_places=2, min_value=Decimal('0.00'))
    sale_price = forms.DecimalField(decimal_places=2, min_value=Decimal('0.00'))
    shopify_id = forms.IntegerField()



class ProductSearchForm(SearchForm):
    name = forms.CharField(required=False)
    sku = forms.CharField(required=False)

    def search(self):
        queryset = self.queryset
        data = self.cleaned_data
        if data['name']:
            queryset = queryset.filter(title__icontains=data['name'])
        if data['sku']:
            queryset = queryset.filter(variants__sku__icontains=data['sku'])
        return queryset.distinct()
