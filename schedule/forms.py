from decimal import Decimal, ROUND_UP
from django import forms

from .models import *
from products.models import Variant


class ScheduleForm(forms.ModelForm):

    theme = forms.ChoiceField(required=False, choices=[])

    class Meta:
        model = Schedule
        fields = ['title', 'date', 'schedule_type', 'discount',
                  'clearance_discount', 'theme', 'coupons', 'exclude_promotion']

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        from products.utils import shopify
        themes = shopify.Theme.find()
        choices = [
            (None, 'None'),
        ]
        for theme in themes:
            choices.append((theme.id, theme.name))
        self.fields['theme'].choices = choices

    def clean_theme(self):
        data = self.cleaned_data['theme']
        if not data:
            return None
        return data

    def clean(self):
        data = super(ScheduleForm, self).clean()
        if data['schedule_type'] in ['storewide', 'collection']:
            if not data.get('discount', 0):
                self.add_error('discount', "Please add a discount rate.")


    def save(self, commit=True):
        instance = super(ScheduleForm, self).save(commit=False)
        if commit:
            instance.save()
            from schedule.tasks import generate_schedule_changes
            generate_schedule_changes.delay(instance.id)
        return instance
