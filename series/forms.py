from django import forms
from django.utils.text import slugify

from .models import *
from products.models import ProductType


class SeriesCreateForm(forms.ModelForm):
    product_types = forms.ModelMultipleChoiceField(
        queryset=ProductType.objects.all(),
        widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Series
        fields = ['title', 'vendor_title', 'description', 'sku', 'vendor',
                  'product_types']

    def save(self, commit=True):
        instance = super(SeriesCreateForm, self).save(commit=False)
        if commit:
            instance.save()
        # Create Products from Product Types
            for product_type in self.cleaned_data['product_types']:
                title = "%s %s" % (self.cleaned_data['title'], product_type.title)
                product = product_type.products.create(
                    title=title.title(), handle=slugify(title),
                    body_html=self.cleaned_data['description'],
                    vendor=self.cleaned_data['vendor'], series=instance)
                variant = product.variants.create(
                    sku="%s-%s" % (self.cleaned_data['sku'], product_type.code)
                )
        return instance
