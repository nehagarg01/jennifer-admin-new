from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^product-update/$', views.ShopifyWebhookProductUpdate.as_view(),
        name='shopify-product-update'),
    # url(r'^create/$', views.ProductCreate.as_view(), name='product-create'),
    # url(r'^(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(), name='product-detail'),
    # url(r'^(?P<pk>[0-9]+)/update$', views.ProductUpdate.as_view(), name='product-update'),
    # url(r'^(?P<pk>[0-9]+)/delete$', views.ProductDelete.as_view(), name='product-delete'),
]
