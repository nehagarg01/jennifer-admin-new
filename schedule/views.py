from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)

from .models import *
from .forms import *


class ScheduleMixin(LoginRequiredMixin):
    model = Schedule


class ScheduleListView(ScheduleMixin, ListView):
    pass


class ScheduleCreateView(ScheduleMixin, CreateView):
    form_class = ScheduleForm
