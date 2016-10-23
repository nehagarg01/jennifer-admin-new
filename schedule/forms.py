from decimal import Decimal, ROUND_UP
from django import forms

from .models import *
from products.models import Variant


class ScheduleForm(forms.ModelForm):

    theme = forms.ChoiceField(required=False, choices=[])

    class Meta:
        model = Schedule
        fields = ['title', 'date', 'schedule_type', 'discount',
                  'clearance_discount', 'theme']

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        from products.utils import shopify
        themes = shopify.Theme.find()
        choices = []
        for theme in themes:
            choices.append((theme.id, theme.name))
        self.fields['theme'].choices = choices

    def clean(self):
        data = super(ScheduleForm, self).clean()
        if data['schedule_type'] in ['storewide', 'collection']:
            if not data.get('discount', 0):
                self.add_error('discount', "Please add a discount rate.")


    # def save(self, commit=True):
    #     instance = super(ScheduleForm, self).save(commit=False)
    #     if commit:
    #         instance.save()
    #         if self.cleaned_data['schedule_type'] == 'storewide':
    #             variants = Variant.main_products.all().values(
    #                 'id', 'compare_at_price', 'price')
    #             discount = Decimal('1.00') - (Decimal(self.cleaned_data['discount']) / Decimal(100))
    #             batch = []
    #             for v in variants:
    #                 sale_price = (v['price'] * discount).quantize(
    #                     Decimal('1.'), rounding=ROUND_UP) - Decimal('0.01')
    #                 c = Change(schedule_id=instance.id, sale_price=sale_price,
    #                            variant_id=v['id'], compare_at_price=v['compare_at_price'],
    #                            price=v['price'])
    #                 batch.append(c)
    #             Change.objects.bulk_create(batch)
    #     return instance
