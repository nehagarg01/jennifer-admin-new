from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product
from .forms import ProductForm


class ProductMixin(LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('product-list')


class ProductList(ProductMixin, ListView):
    pass


class ProductFormMixin(ProductMixin):
    form_class = ProductForm

    def form_valid(self, form):
        product = form.save()
        product.attributes.clear()
        attributes = form.cleaned_data['style'] | form.cleaned_data['material']\
            | form.cleaned_data['feature']
        for att in attributes:
            product.attributes.add(att)
        return super(ProductFormMixin, self).form_valid(form)


class ProductCreate(ProductFormMixin, CreateView):
    pass


class ProductDetail(ProductMixin, DetailView):
    pass


class ProductUpdate(ProductFormMixin, UpdateView):
    pass


class ProductDelete(ProductMixin, DeleteView):
    pass
