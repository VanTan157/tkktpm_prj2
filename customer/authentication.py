from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Customer

class CustomerJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Tùy chỉnh hàm get_user để truy vấn Customer theo 'user_id' trong token.
        Nếu token của bạn chứa email thay vì user_id, bạn có thể sửa lại truy vấn.
        """
        try:
            # Giả sử token chứa 'user_id' (ID của Customer)
            user_id = validated_token.get("user_id")
            if user_id is None:
                raise AuthenticationFailed("Token không chứa user_id", code="user_id_missing")
            # Tìm kiếm Customer theo id
            user = Customer.objects.get(id=user_id)
        except Customer.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")
        return user
