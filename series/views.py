from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)
from django.core.urlresolvers import reverse_lazy, reverse

from .models import *


class SeriesMixin(LoginRequiredMixin):
    model = Series
    fields = ['title', 'vendor_title', 'description', 'sku', 'vendor']


class SeriesListView(SeriesMixin, ListView):
    pass


class SeriesCreateView(SeriesMixin, CreateView):
    pass


class SeriesUpdateView(SeriesMixin, UpdateView):
    pass


class SeriesDetailView(SeriesMixin, DetailView):
    pass
