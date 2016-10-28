from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView, FormView)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory, modelformset_factory
from django.conf import settings

import shopify
from .utils import shopify

from .models import *
from schedule.models import Change
from .forms import ProductForm, ProductScheduleChangeForm, ProductSearchForm
from core.views import SearchView


class ProductMixin(LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('product-list')


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
         context['changes'] = Change.objects.filter(
            variant__product=self.object).order_by('schedule__date')
         return context


class ProductUpdate(ProductFormMixin, UpdateView):

    def get_success_url(self):
        product = shopify.Product.find(self.object.shopify_id)
        for k in ['title', 'body_html']:
            setattr(product, k, getattr(self.object, k))
        product.save()
        return super(ProductUpdate, self).get_success_url()


class ProductDelete(ProductMixin, DeleteView):
    pass


class ProductScheduleChange(ProductMixin, DetailView):
    form_class = ProductScheduleChangeForm
    template_name = 'products/product_schedule_change.html'

    def get_context_data(self, **kwargs):
        context = super(ProductScheduleChange, self).get_context_data(**kwargs)
        context['form'] = ProductScheduleChangeForm
        ChangeFormSet = modelformset_factory(
            Change, fields=('compare_at_price', 'price', 'sale_price', 'variant'),
            extra=self.object.variants.count())
        context['formset'] = ChangeFormSet(queryset=Change.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ProductScheduleChangeForm(request.POST)
        formset = modelformset_factory(
            Change, fields=('compare_at_price', 'price', 'sale_price', 'variant'),
            extra=self.object.variants.count())
        formset = formset(request.POST)
        if form.is_valid() and formset.is_valid():
            for f in formset:
                f.instance.schedule = form.cleaned_data['schedule']
                f.save()
            return redirect('product-detail', self.object.pk)
        return redirect('product-schedule-change', self.object.pk)

    def get_success_url(self):
        return self.product.get_absolute_url()
