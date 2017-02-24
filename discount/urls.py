from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^export/$', views.ExportDiscount.as_view(), name="export-discount"),
]
