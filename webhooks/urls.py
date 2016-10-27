from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ShopifyWebhookView.as_view(),
        name='shopify-webhook'),
    url(r'^product-update/$', views.ShopifyWebhookProductUpdate.as_view(),
        name='shopify-product-update'),
]
