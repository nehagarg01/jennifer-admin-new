import csv
from decimal import Decimal, ROUND_UP

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView, FormView, RedirectView)

from .forms import *


class ExportDiscount(FormView):
    form_class = DiscountForm
    template_name = 'discount/export_discount.html'

    def form_valid(self, form):
        reader = csv.reader(form.cleaned_data['file'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="parsed.csv"'
        writer = csv.writer(response)

        handle = ""
        exclude = []
        if form.cleaned_data['exclude_tags']:
            for tag in form.cleaned_data['exclude_tags'].split(","):
                exclude.append(tag.strip())

        discount = Decimal(100 - form.cleaned_data['discount']) / Decimal(100)
        if form.cleaned_data['exclude_closeout']:
            exclude.append('clearance')

        for idx, row in enumerate(reader):
            if idx > 0 and row[0] and row[0] not in ['guardsman-5-year-elite-plan', 'gift-card']:
                if row[5] and not any(x in row[5] for x in exclude):
                    handle = row[0]
                if row[0] == handle:
                    try:
                        row[19] = (Decimal(row[19]) * discount).quantize(
                            Decimal('1.'), rounding=ROUND_UP) - Decimal('0.01')
                    except:
                        pass
            writer.writerow(row)
        return response
