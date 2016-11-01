from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy, reverse

from .models import *
from .forms import *


class ScheduleMixin(LoginRequiredMixin):
    model = Schedule
    success_url = reverse_lazy('schedule-list')


class ScheduleListView(ScheduleMixin, ListView):
    pass


class ScheduleCreateView(ScheduleMixin, CreateView):
    form_class = ScheduleForm


class ScheduleDeleteView(ScheduleMixin, DeleteView):
    pass


class ScheduleExecute(ScheduleMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        schedule = get_object_or_404(Schedule, pk=kwargs['pk'])
        schedule.run_schedule()
        return reverse('schedule-list')


class ChangeDeleteView(LoginRequiredMixin, DeleteView):
    model = Change

    def get_success_url(self):
        return self.object.product.get_absolute_url()


class ChangeListView(LoginRequiredMixin, ListView):
    model = Change
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Schedule, pk=self.kwargs.get('pk'))
        return super(ChangeListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(ChangeListView, self).get_queryset().filter(schedule=self.object)

    def get_context_data(self, **kwargs):
        context = super(ChangeListView, self).get_context_data(**kwargs)
        context['object'] = self.object
        return context
