from django.contrib import admin
from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

# router = routers.DefaultRouter()
# router.register('bus-company', views.BusCompanyViewSet)
# router.register('user', views.UserViewSet)
# router.register('ticket', views.TicketViewSet)
# router.register('delivery', views.DeliveryViewSet)
# router.register('revenue-statistics', views.RevenueStatisticsViewSet)
# router.register('bus-route', views.BusRouteViewSet)
# router.register('trip', views.TripViewSet)
# router.register('user-ticket', views.UserTicketViewSet)
urlpatterns = [
    # path('', views.index, name="index"),
    # path('', include(router.urls)),
    path('', views.home, name="home"),
    path('dat-ve/<int:trip_id>/', views.booking, name="booking"),
    path('lich-trinh/', views.schedule, name="schedule"),
    path('tra-cuu-ve/', views.ticket_search, name="ticket_search"),
    path('lien-he/', views.contact, name="contact"),
    path('ve-chung-toi/', views.about, name="about"),
    path('ket-qua-tim-kiem/', views.search_trip, name="search_trip"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('thanh-toan/', views.zalo_payment, name='payment'),
    path('thanh-toan-thanh-cong/', views.payment_success, name='payment_success'),
    path('thong-tin-ca-nhan/', views.profile_view, name='profile'),
    path('email/', views.send_email, name='email'),
    path('social-auth/', include('social_django.urls', namespace='social')),


    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin_site.urls),
    # path('search-trip/', views.TripViewSet.as_view({'get': 'search_trip'}), name='search-trip'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
