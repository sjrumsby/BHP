from django.conf.urls  import url, include
from django.contrib import admin
admin.autodiscover()

from hockeypool import views

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index')
]
