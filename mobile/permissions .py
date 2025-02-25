from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Chỉ cho phép user có kiểu admin (ví dụ: customer_type == 'admin') thực hiện các hành động thay đổi.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'customer_type', None) == 'admin'
