from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Vendor


class VendorMixin(LoginRequiredMixin):
    model = Vendor
    fields = ['code', 'name', 'contact_person', 'email', 'phone']
    success_url = reverse_lazy('vendor-list')


class VendorList(VendorMixin, ListView):
    pass


class VendorCreate(VendorMixin, CreateView):
    pass


class VendorUpdate(VendorMixin, UpdateView):
    pass


class VendorDelete(VendorMixin, DeleteView):
    pass
