from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)
from django.core.urlresolvers import reverse_lazy, reverse

from .models import *
from .forms import SeriesCreateForm


class SeriesMixin(LoginRequiredMixin):
    model = Series



class SeriesListView(SeriesMixin, ListView):
    pass


class SeriesCreateView(SeriesMixin, CreateView):
    form_class = SeriesCreateForm


class SeriesUpdateView(SeriesMixin, UpdateView):
    fields = ['title', 'vendor_title', 'description', 'sku', 'vendor']


class SeriesDetailView(SeriesMixin, DetailView):
    pass
