from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from dashboard.views import Dashboard


urlpatterns = [
    url(r'^$', Dashboard.as_view(), name="dashboard"),
    url(r'^index/$', Dashboard.as_view(), name="index"),
    url(r'^accounts/', include('authentication.urls', namespace='user')),
    url(r'^vendors/', include('vendors.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^series/', include('series.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^webhooks/', include('webhooks.urls')),
    url(r'^discount/', include('discount.urls')),
]
