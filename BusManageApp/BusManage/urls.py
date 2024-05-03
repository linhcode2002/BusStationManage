from django.contrib import admin
from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework import routers

router = routers.DefaultRouter()
router.register('bus-company', views.BusCompanyViewSet)
router.register('user', views.UserViewSet)
urlpatterns = [
    # path('', views.index, name="index"),
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin_site.urls),
]