from django.conf.urls import url, include

from shopify_webhook.views import WebhookView

from . import views


urlpatterns = [
    url(r'^$', WebhookView.as_view(), name="webhooks"),
    url(r'^carrier/$', views.carrier_webhook, name='carrier-calculate'),
    url(r'^zipcode/$', views.ZipcodeParse.as_view(), name='zipcode-parse'),
]
