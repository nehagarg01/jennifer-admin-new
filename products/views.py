from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory

from .models import *
from .forms import ProductForm


class ProductMixin(LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('product-list')


class ProductList(ProductMixin, ListView):
    paginate_by = 25


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
    pass


class ProductUpdate(ProductFormMixin, UpdateView):
    pass


class ProductDelete(ProductMixin, DeleteView):
    pass
