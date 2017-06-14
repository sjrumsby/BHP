from django.conf.urls  import url, include
from rest_framework_jwt.views import obtain_jwt_token
from api import views

urlpatterns = [
    url(r'^api-token-auth/$', obtain_jwt_token),
]
