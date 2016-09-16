from django import forms

from .models import Product, ProductAttribute


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
