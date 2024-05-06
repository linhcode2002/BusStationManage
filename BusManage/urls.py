from django.contrib import admin
from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework import routers

router = routers.DefaultRouter()
router.register('bus-company', views.BusCompanyViewSet)
router.register('user', views.UserViewSet)
router.register('ticket', views.TicketViewSet)
router.register('delivery', views.DeliveryViewSet)
router.register('revenue-statistics', views.RevenueStatisticsViewSet)
router.register('bus-route', views.BusRouteViewSet)
router.register('trip', views.TripViewSet)
urlpatterns = [
    # path('', views.index, name="index"),
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin_site.urls),
]