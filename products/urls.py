from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.ProductList.as_view(), name='product-list'),
    url(r'^create/$', views.ProductCreate.as_view(), name='product-create'),
    url(r'^parse/$', views.ProductParse.as_view(), name='product-parse'),
    url(r'^(?P<pk>[0-9]+)/', include([
        url(r'^$', views.ProductDetail.as_view(), name='product-detail'),
        url(r'^update/$', views.ProductUpdate.as_view(), name='product-update'),
        url(r'^delete/$', views.ProductDelete.as_view(), name='product-delete'),
        url(r'^schedule/$', views.ProductScheduleChange.as_view(), name='product-schedule-change'),
        url(r'^variants/$', views.ProductVariantsUpdateView.as_view(), name='product-variants-update'),
        url(r'^push/$', views.ProductPushShopifyView.as_view(), name='product-push'),
        url(r'^pull/$', views.ProductPullShopifyView.as_view(), name='product-pull'),
    ])),
]
