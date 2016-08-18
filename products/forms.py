from django import forms

from .models import Product, ProductAttribute


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'body_html', 'handle', 'product_type', 'vendor',
                  'material', 'style', 'feature']

    material = forms.ModelMultipleChoiceField(
        queryset=ProductAttribute.objects.filter(attribute_type="MA"))
    style = forms.ModelMultipleChoiceField(
        queryset=ProductAttribute.objects.filter(attribute_type="ST"))
    feature = forms.ModelMultipleChoiceField(
        queryset=ProductAttribute.objects.filter(attribute_type="FT"),
        required=False)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['material'].initial = self.instance.attributes.filter(
                attribute_type="MA")
            self.fields['style'].initial = self.instance.attributes.filter(
                attribute_type="ST")
            self.fields['feature'].initial = self.instance.attributes.filter(
                attribute_type="FT")
