from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
from authentication.urls import urlpatterns as user_urls

# Examples:
# url(r'^$', 'core.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^accounts/', include(user_urls, namespace='user')),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
