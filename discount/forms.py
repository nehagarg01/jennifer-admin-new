from decimal import Decimal

from django import forms


class DiscountForm(forms.Form):
    file = forms.FileField()
    discount = forms.IntegerField()
    exclude_closeout = forms.BooleanField(required=False)
    exclude_tags = forms.CharField(required=False,
                                   help_text="Use commas between tags")
