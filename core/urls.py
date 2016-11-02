from django.conf.urls import include, url

from shopify_webhook.views import WebhookView
from django.contrib import admin
admin.autodiscover()

from dashboard.views import Dashboard
from .views import CarrierView


urlpatterns = [
    url(r'^$', Dashboard.as_view(), name="dashboard"),
    url(r'^accounts/', include('authentication.urls', namespace='user')),
    url(r'^vendors/', include('vendors.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^series/', include('series.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^webhooks/', WebhookView.as_view(), name="webhooks"),
    url(r'^carrier/$', CarrierView.as_view(), name='carrier-calculate'),
]
