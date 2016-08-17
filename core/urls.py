from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from authentication.urls import urlpatterns as user_urls
from dashboard.views import Dashboard
from vendors.urls import urlpatterns as vendor_urls

# Examples:
# url(r'^$', 'core.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^accounts/', include(user_urls, namespace='user')),
    url(r'^dashboard', Dashboard.as_view(), name="dashboard"),
    url(r'^vendors/', include(vendor_urls)),
    url(r'^admin/', include(admin.site.urls)),
]
