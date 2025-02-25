from rest_framework import permissions

class IsAdminCustomer(permissions.BasePermission):
    """
    Cho phép truy cập nếu người dùng đã được xác thực và có customer_type là 'admin'.
    """
    def has_permission(self, request, view):
        # Kiểm tra người dùng đã đăng nhập và customer_type của họ là admin.
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'customer_type', None) == 'admin')
