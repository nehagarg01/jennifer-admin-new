from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ProductList.as_view(), name='product-list'),
    url(r'^create/$', views.ProductCreate.as_view(), name='product-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(), name='product-detail'),
    url(r'^(?P<pk>[0-9]+)/update$', views.ProductUpdate.as_view(), name='product-update'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.ProductDelete.as_view(), name='product-delete'),
]
