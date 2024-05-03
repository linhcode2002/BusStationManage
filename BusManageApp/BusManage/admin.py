from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib.auth.models import Permission, Group
from .models import User, BusCompany, BusRoute, Trip, Ticket, Delivery, Review, RevenueStatistics
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.urls import path

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'first_name', 'last_name', 'email', 'is_active']
    search_fields = ['username', 'first_name', 'first_name', 'last_name', 'email']
    list_filter = ['is_active']
    readonly_fields = ["image"]

    def image(self, obj):
        if obj:
            return mark_safe(
                "<img src='{url}' width='120' />".format(url=obj.avatar.url)
            )
class BusCompanyForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = BusCompany
        fields = '__all__'

class BusCompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active']
    search_fields = ['name']
    list_filter = ['active', 'name']
    form = BusCompanyForm
    readonly_fields = ["image"]

    def image(self, obj):
        if obj:
            return mark_safe(
                "<img src='/static/{url}' width='120' />".format(url=obj.avatar.name)
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

admin_site = BusManageAdminSite('mybusmanage')

admin_site.register(User, UserAdmin)
admin_site.register(BusCompany, BusCompanyAdmin)
admin_site.register(BusRoute)
admin_site.register(Trip)
admin_site.register(Ticket)
admin_site.register(Delivery)
admin_site.register(Review)
admin_site.register(RevenueStatistics)
admin_site.register(Group)
admin_site.register(Permission)