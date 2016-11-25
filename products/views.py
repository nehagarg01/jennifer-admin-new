import json
import csv

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView, FormView, RedirectView)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory, modelformset_factory, formset_factory
from django.conf import settings
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now, localtime
from django.http import HttpResponse

from extra_views import InlineFormSetView, FormSetView

import shopify
from .utils import shopify
from .models import *
from schedule.models import Change
from .forms import *
from core.views import SearchView
from core.forms import FileForm


class ProductMixin(LoginRequiredMixin):
    model = Product

    def update_to_shopify(self):
        success, error = self.object.update_to_shopify()
        if success:
            messages.success(self.request, "Updated to Shopify")
        else:
            messages.error(self.request,
                           "Unable to update to shopify. %s" % error.full_messages())


class ProductList(ProductMixin, SearchView):
    search_form = ProductSearchForm
    paginate_by = 20


class ProductFormMixin(ProductMixin):
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super(ProductFormMixin, self).get_context_data(**kwargs)
        DimensionFormSet = inlineformset_factory(
            Product, Dimension, fields=('title', 'width', 'depth', 'height'), extra=1)
        context['formset'] = DimensionFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        DimensionFormSet = inlineformset_factory(
            Product, Dimension, fields=('title', 'width', 'depth', 'height'), extra=1)
        formset = DimensionFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            product = form.save()
            product.attributes.clear()
            attributes = form.cleaned_data['styles'] | form.cleaned_data['materials']\
                | form.cleaned_data['features']
            product.attributes.add(*list(attributes))
            formset.save()
        else:
            context = self.get_context_data()
            context.update({'form': form, 'formset': formset})
            return self.render_to_response(context)
        return super(ProductFormMixin, self).form_valid(form)


class ProductCreate(ProductFormMixin, CreateView):
    pass


class ProductDetail(ProductMixin, DetailView):

     def get_context_data(self, **kwargs):
         context = super(ProductDetail, self).get_context_data(**kwargs)
         context['changes'] = self.object.changes.filter(
            completed=False, schedule__date__gte=localtime(now()).date())
         return context


class ProductUpdate(ProductFormMixin, UpdateView):

    def get_success_url(self):
        self.update_to_shopify()
        return super(ProductUpdate, self).get_success_url()


class ProductVariantsUpdateView(ProductMixin, InlineFormSetView):
    template_name = 'products/product_variants_form.html'
    inline_model = Variant
    fields = ['sku', 'option1', 'option2', 'option3',
              'sale_price', 'price', 'compare_at_price',
              'barcode', 'pieces']
    can_delete = True

    def get_success_url(self):
        self.update_to_shopify()
        return self.object.get_absolute_url()


class ProductDelete(ProductMixin, DeleteView):
    success_url = reverse_lazy('product-list')


class ProductScheduleChange(ProductMixin, DetailView):
    form_class = ProductScheduleChangeForm
    template_name = 'products/product_schedule_change.html'

    def get_context_data(self, **kwargs):
        context = super(ProductScheduleChange, self).get_context_data(**kwargs)
        context['form'] = ProductScheduleChangeForm
        ChangeFormSet = formset_factory(form=ChangeForm, extra=0)
        initial = []
        for variant in self.object.variants.all():
            initial.append({
                'title': str(variant),
                'shopify_id': variant.shopify_id,
                'price': variant.price,
                'compare_at_price': variant.compare_at_price,
                'sale_price': variant.sale_price,
            })
        context['formset'] = ChangeFormSet(initial=initial)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ProductScheduleChangeForm(request.POST)
        formset = formset_factory(form=ChangeForm)
        formset = formset(request.POST)
        if form.is_valid() and formset.is_valid():
            for data in formset.cleaned_data:
                # data['id'] = data.pop('shopify_id')
                for k in ['price', 'sale_price', 'compare_at_price']:
                    data[k] = float(data[k])

            # print formset.cleaned_data
            Change.objects.create(
                product=self.object, schedule=form.cleaned_data['schedule'],
                json=formset.cleaned_data)
            return redirect('product-detail', self.object.pk)
        return redirect('product-schedule-change', self.object.pk)

    def get_success_url(self):
        return self.product.get_absolute_url()


class ProductParse(FormView):
    form_class = FileForm
    template_name = 'products/product_parse.html'

    def form_valid(self, form):
        reader = csv.reader(form.cleaned_data['file'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="parsed.csv"'
        writer = csv.writer(response)
        for idx, row in enumerate(reader):
            if idx >= 6 and row[3]:
                p = Product.objects.filter(gmc_id__icontains=row[3]).first()
                if p:
                    row[3] = p.title
            writer.writerow(row)
        return response


class ProductPushShopifyView(ProductMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        product.update_to_shopify(override=True)
        return product.get_absolute_url()


class ProductPullShopifyView(ProductMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        product.pull()
        return product.get_absolute_url()
