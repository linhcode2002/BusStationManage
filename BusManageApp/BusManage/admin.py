from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.template.response import TemplateResponse
from django.contrib.auth.models import Permission, Group
from .models import *
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.urls import path


# Register your models here.
class UserAdminForm(forms.ModelForm):
    reset_password = forms.CharField(label='Reset Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = '__all__'
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'first_name', 'last_name', 'email', 'is_active']
    search_fields = ['username', 'first_name', 'first_name', 'last_name', 'email']
    list_filter = ['is_active']
    readonly_fields = ["image"]
    form = UserAdminForm

    def image(self, obj):
        if obj:
            return mark_safe(
                "<img src='{url}' width='120' />".format(url=obj.avatar.url)
            )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created
            obj.password = make_password(form.cleaned_data['password'])
        reset_password = form.cleaned_data.get('reset_password')
        if reset_password:  # Nếu người dùng nhập mật khẩu mới
            obj.password = make_password(reset_password)
        super().save_model(request, obj, form, change)
class BusCompanyForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = BusCompany
        fields = '__all__'


class BusCompanyInline(admin.StackedInline):
    model = BusCompany
    extra = 0  # Số lượng form rỗng hiển thị
class TripInline(admin.StackedInline):
    model = Trip
    extra = 0  # Số lượng form rỗng hiển thị

class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 0

class DeliveryInline(admin.StackedInline):
    model = Delivery
    extra = 0

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0

class CommentsInline(admin.StackedInline):
    model = Comments
    extra = 0

class RevenueStatisticsInline(admin.StackedInline):
    model = RevenueStatistics
    extra = 0

class LikeInline(admin.StackedInline):
    model = Like
    extra = 0

class BusRouterInline(admin.StackedInline):
    model = BusRoute
    extra = 0

class BusCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'created_date', 'updated_date']
    search_fields = ['name']
    list_filter = ['active', 'name']
    form = BusCompanyForm
    readonly_fields = ["image"]
    inlines = [BusRouterInline, CommentsInline, LikeInline, RevenueStatisticsInline]

    def image(self, obj):
        if obj:
            return mark_safe(
                "<img src='{url}' width='120' />".format(url=obj.avatar.url)
            )

class BusManageAdminSite(admin.AdminSite):
    site_header = "HỆ THỐNG QUẢN LÝ BẾN XE BUS"

    def get_urls(self):
        return [
            path('bus-manage-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/bus-manage-stats.html', {

        })
class BusRouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus_company', 'route_name', 'start_location', 'end_location']
    search_fields = ['route_name', 'start_location', 'end_location']
    list_filter = ['bus_company']

class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus_route', 'departure_time', 'arrival_time', 'ticket_price']
    search_fields = ['bus_route__route_name']
    list_filter = ['bus_route']

class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'trip', 'active', 'created_date', 'updated_date', 'remaining_seats', 'total_seats']
    search_fields = ['trip__bus_route__route_name', 'user__username']
    list_filter = ['remaining_seats', 'total_seats', 'active']

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender_name', 'receiver_name', 'delivery_time', 'pickup_time', 'delivery_status', 'bus_company']
    search_fields = ['sender_name', 'receiver_name', 'delivery_status', 'bus_company__name']
    list_filter = ['delivery_status', 'bus_company']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bus_company', 'rating']
    search_fields = ['user__username', 'bus_company__name']
    list_filter = ['bus_company']

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bus_company', 'comment']
    search_fields = ['user__username', 'bus_company__name']

class RevenueStatisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'bus_company', 'month', 'year', 'revenue', 'frequency']
    search_fields = ['bus_company__name']
    list_filter = ['bus_company']

class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bus_company', 'active']
    search_fields = ['user__username', 'bus_company__name']
    list_filter = ['active']

class UserTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'active', 'payment_status', 'is_online_booking', 'quantity', 'ticket', 'total_price']
    search_fields = ['payment_status', 'quantity']
    list_filter = ['active']


admin_site = BusManageAdminSite('mybusmanage')

admin_site.register(User, UserAdmin)
admin_site.register(BusCompany, BusCompanyAdmin)
admin_site.register(BusRoute, BusRouteAdmin)
admin_site.register(Trip, TripAdmin)
admin_site.register(Ticket, TicketAdmin)
admin_site.register(Delivery, DeliveryAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(Comments, CommentsAdmin)
admin_site.register(RevenueStatistics, RevenueStatisticsAdmin)
admin_site.register(Like, LikeAdmin)
admin_site.register(Permission)
admin_site.register(Group)
admin_site.register(UserTicket, UserTicketAdmin)