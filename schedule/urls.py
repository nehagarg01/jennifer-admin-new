from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.ScheduleListView.as_view(), name='schedule-list'),
    url(r'^create/$', views.ScheduleCreateView.as_view(), name='schedule-create'),
    url(r'^(?P<pk>[0-9]+)/', include([
        url(r'^$', views.ChangeListView.as_view(), name='schedule-detail'),
        url(r'^execute/$', views.ScheduleExecute.as_view(), name='schedule-execute'),
        # url(r'^(?P<pk>[0-9]+)/update$', views.ProductUpdate.as_view(), name='product-update'),
        url(r'^delete/$', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
    ])),
    url(r'^changes/(?P<pk>[0-9]+)/', include([
        url(r'^delete/$', views.ChangeDeleteView.as_view(), name='change-delete'),
    ])),
]
