from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^jet/', include('jet.urls', namespace='jet')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('app.urls', namespace='app')),
]
