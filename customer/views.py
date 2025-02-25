from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework_simplejwt.views import TokenViewBase
from .serializers import CustomerTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CustomerSerializer
from .permissions import IsAdminCustomer  
from rest_framework.exceptions import PermissionDenied

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Sau khi xác thực, request.user sẽ là instance của Customer
        serializer = CustomerSerializer(request.user)
        return Response(serializer.data)

class CustomerTokenObtainPairView(TokenViewBase):
    serializer_class = CustomerTokenObtainPairSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Customer
from .serializers import CustomerSerializer, CustomerTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.views import APIView
from .permissions import IsAdminCustomer  # Giả sử bạn đặt IsAdminCustomer vào file permissions.py

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # GET: Yêu cầu phải xác thực và là admin
            return [IsAuthenticated(), IsAdminCustomer()]
        # POST: Không yêu cầu xác thực token
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'password' not in data or not data['password']:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
        data['password'] = make_password(data['password'])  # Mã hóa mật khẩu
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)  # Sử dụng 200 thay vì 201




from rest_framework import mixins

class CustomerDetailView(mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.customer_type != 'admin' and obj.id != user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Bạn không có quyền sửa thông tin của người khác.")
        return obj

    def put(self, request, *args, **kwargs):
        # Sử dụng update mixin, sau đó ép trả về status 200
        response = self.update(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        # Nếu cần trả về status 200 thay vì 204, bạn có thể làm như sau:
        return Response({"detail": "Deleted successfully."}, status=status.HTTP_200_OK)
