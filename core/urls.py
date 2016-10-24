from django.conf.urls import include, url

from webhooks.views import ShopifyWebhookView
from django.contrib import admin
admin.autodiscover()

from dashboard.views import Dashboard


urlpatterns = [
    url(r'^$', Dashboard.as_view(), name="dashboard"),
    url(r'^accounts/', include('authentication.urls', namespace='user')),
    url(r'^vendors/', include('vendors.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^webhook/', include('webhooks.urls', namespace='webhooks')),
]
