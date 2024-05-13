from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated

class OwnerPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user == obj.user


class IsBusCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='bus_company').exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='admin').exists()

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='user').exists()

class EditPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='bus_company').exists():
            return obj.bus_company.admin_user == request.user
        return False

class EditTicketPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='bus_company').exists():
            return obj.trip.bus_company.admin_user == request.user
        return False

class IsBusCompanyOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Không cần đăng nhập vẫn có thể xem buscompany, like, comment
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Phải đăng nhập mới thêm được like và comment
        if request.method in ['POST']:
            return request.user.is_authenticated
        # user thuộc group bus_company có thể xem, thêm, sửa, xóa tất cả BusCompany, Like, Comment
        if request.user.groups.filter(name='bus_company').exists():
            return True
        # user thuộc group user có thể xem BusCompany và xem, thêm, sửa, xóa tất cả, Like, Comment
        if request.user.groups.filter(name='user').exists():
            return True
        # user admin thì có full quyền
        if request.user.groups.filter(name='admin').exists():
            return True
        return False
