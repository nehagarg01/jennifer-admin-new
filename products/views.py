from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product


class ProductMixin(LoginRequiredMixin):
    model = Product
    fields = ['title', 'body_html', 'handle', 'product_type', 'vendor']
    success_url = reverse_lazy('product-list')


class ProductList(ProductMixin, ListView):
    pass


class ProductCreate(ProductMixin, CreateView):
    pass


class ProductDetail(ProductMixin, DetailView):
    pass


class ProductUpdate(ProductMixin, UpdateView):
    pass


class ProductDelete(ProductMixin, DeleteView):
    pass
