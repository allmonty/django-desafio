from django.conf.urls import include, url

from django.contrib import admin

admin.autodiscover()

import api.views

urlpatterns = [
    url(r'^api/', include('api.urls'), name='api'),
    url(r'^admin/', include(admin.site.urls)),
]
