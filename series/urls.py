from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.SeriesListView.as_view(), name='series-list'),
    url(r'^create/$', views.SeriesCreateView.as_view(), name='series-create'),
    url(r'^(?P<pk>[0-9]+)/', include([
        url(r'^$', views.SeriesDetailView.as_view(), name='series-detail'),
        url(r'^update/$', views.SeriesUpdateView.as_view(), name='series-update'),
        # url(r'^(?P<pk>[0-9]+)/update$', views.ProductUpdate.as_view(), name='product-update'),
        # url(r'^delete/$', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
    ])),
]
