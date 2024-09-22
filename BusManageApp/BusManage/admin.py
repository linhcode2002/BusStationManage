from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.template.response import TemplateResponse
from django.contrib.auth.models import Permission, Group
from .models import *
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.urls import path

# Đăng ký form người dùng để quản lý thay đổi mật khẩu
class UserAdminForm(forms.ModelForm):
    reset_password = forms.CharField(label='Reset Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = '__all__'

# Quản lý User trong admin
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['is_active']
    readonly_fields = ["image"]
    form = UserAdminForm

    def image(self, obj):
        if obj and obj.avatar:
            return mark_safe(
                "<img src='{url}' width='120' />".format(url=obj.avatar.url)
            )
        return "(No image)"

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Nếu đối tượng mới được tạo
            obj.password = make_password(form.cleaned_data['password'])
        reset_password = form.cleaned_data.get('reset_password')
        if reset_password:  # Nếu người dùng nhập mật khẩu mới
            obj.password = make_password(reset_password)
        super().save_model(request, obj, form, change)

# Inline quản lý chuyến xe
class TripInline(admin.StackedInline):
    model = Trip
    extra = 0  # Không thêm form rỗng

# Quản lý tuyến xe
class BusRouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'route_name', 'start_location', 'end_location', 'distance']
    search_fields = ['route_name', 'start_location', 'end_location']
    list_filter = ['route_name']
    inlines = [TripInline]  # Gắn inline cho các chuyến xe

# Quản lý chuyến xe
class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus_route', 'departure_time', 'arrival_time', 'ticket_price']
    search_fields = ['bus_route__route_name']
    list_filter = ['bus_route']

# Quản lý thống kê doanh thu
class RevenueStatisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'month', 'year', 'revenue', 'frequency']
    search_fields = ['month', 'year']
    list_filter = ['month', 'year']

# Quản lý đánh giá
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'title', 'customer_email', 'phone_number']
    search_fields = ['customer_email']
    list_filter = ['name']

# Quản lý thống kê chuyến xe
class TripStatisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'trip', 'total_tickets', 'booked_tickets', 'total_payment']
    search_fields = ['trip__bus_route__route_name']
    list_filter = ['trip__bus_route']

# Quản lý bến xe riêng
class BusManageAdminSite(admin.AdminSite):
    site_header = "HỆ THỐNG QUẢN LÝ BẾN XE BUS"

    def get_urls(self):
        return [
            path('bus-manage-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/bus-manage-stats.html', {})

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_number', 'email', 'address']
    search_fields = ['name', 'phone_number', 'email']
    list_filter = ['name', 'email']
    readonly_fields = ["image"]

    def image(self, obj):
        if obj and obj.avatar:
            return mark_safe(
                "<img src='{url}' width='120' />".format(url=obj.avatar.url)
            )
        return "(No image)"

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Nếu là tạo mới
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

# Quản lý xe bus
class BusAdmin(admin.ModelAdmin):
    list_display = ['id', 'license_plate', 'total_seats', 'driver']
    search_fields = ['license_plate', 'driver']
    list_filter = ['license_plate']

# Quản lý ghế ngồi
class SeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'bus']
    search_fields = ['name', 'bus__license_plate']
    list_filter = ['bus']

# Quản lý việc đặt vé
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'trip', 'seat', 'customer_name', 'customer_email', 'booking_time']
    search_fields = ['customer_name', 'customer_email', 'trip__bus_route__route_name', 'seat__name']
    list_filter = ['trip__bus_route', 'booking_time']

# Tạo site quản lý riêng
admin_site = BusManageAdminSite('mybusmanage')

# Đăng ký các model vào admin
admin_site.register(User, UserAdmin)
admin_site.register(BusRoute, BusRouteAdmin)
admin_site.register(Trip, TripAdmin)
admin_site.register(TripStatistics, TripStatisticsAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(RevenueStatistics, RevenueStatisticsAdmin)
admin_site.register(Permission)
admin_site.register(Group)
admin_site.register(Customer, CustomerAdmin)
admin_site.register(Bus, BusAdmin)
admin_site.register(Seat, SeatAdmin)
admin_site.register(Booking, BookingAdmin)
