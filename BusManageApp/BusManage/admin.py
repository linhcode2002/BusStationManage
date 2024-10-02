from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.template.response import TemplateResponse
from django.contrib.auth.models import Permission, Group
from .models import *
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.urls import path
from social_django.models import UserSocialAuth

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

class BusRouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'route_name', 'start_location', 'end_location', 'distance', 'active']
    search_fields = ['route_name', 'start_location', 'end_location']
    list_filter = ['route_name', 'active']
    inlines = [TripInline]  # Gắn inline cho các chuyến xe

# Quản lý chuyến xe
class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus_route', 'departure_time', 'arrival_time', 'ticket_price', 'active']
    search_fields = ['bus_route__route_name']
    list_filter = ['bus_route', 'active']

# Quản lý thống kê doanh thu
class RevenueStatisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'month', 'year', 'revenue', 'frequency', 'active']
    search_fields = ['month', 'year']
    list_filter = ['month', 'year', 'active']

# Quản lý đánh giá
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'title', 'customer_email', 'phone_number', 'active']
    search_fields = ['customer_email']
    list_filter = ['name', 'active']

# Quản lý thống kê chuyến xe
class TripStatisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'trip', 'total_tickets', 'booked_tickets', 'total_payment', 'active']
    search_fields = ['trip__bus_route__route_name']
    list_filter = ['trip__bus_route', 'active']

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
    list_display = ['id', 'name', 'phone_number', 'email', 'address', 'active']
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
    list_display = ['id', 'license_plate', 'total_seats', 'driver', 'active']
    search_fields = ['license_plate', 'driver']
    list_filter = ['license_plate', 'active']

# Quản lý ghế ngồi
class SeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'bus', 'active']
    search_fields = ['name']
    list_filter = ['active']
# Quản lý việc đặt vé
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'trip', 'ticket_code', 'customer_name', 'customer_email', 'booking_time', 'seat']
    search_fields = ['customer_name', 'customer_email', 'ticket_code', 'trip__bus_route__route_name']
    list_filter = ['trip__bus_route', 'booking_time']


    def get_seat_names(self, obj):
        return ", ".join([seat.name for seat in obj.seats.all()])  # Hiển thị danh sách ghế
    get_seat_names.short_description = 'Seats'  # Tiêu đề cột hiển thị trong admin

    def save_model(self, request, obj, form, change):
        # Kiểm tra số lượng ghế
        if form.cleaned_data['seats'].count() > 4:
            raise ValueError("Chỉ được đặt tối đa 4 ghế.")

        # Lưu đối tượng
        super().save_model(request, obj, form, change)

class SocialAuthAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'provider', 'uid']
    search_fields = ['user__username', 'user__email', 'provider', 'uid']
    list_filter = ['provider']

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
admin_site.register(UserSocialAuth, SocialAuthAdmin)  # Đăng ký UserSocialAuth