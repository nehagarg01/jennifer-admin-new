from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.VendorList.as_view(), name='vendor-list'),
    url(r'^create/$', views.VendorCreate.as_view(), name='vendor-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.VendorUpdate.as_view(), name='vendor-update'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.VendorDelete.as_view(), name='vendor-delete'),
]
