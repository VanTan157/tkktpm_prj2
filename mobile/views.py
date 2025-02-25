from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Mobile
from .serializers import MobileSerializer
from customer.permissions import IsAdminCustomer# Custom permission đã định nghĩa

class MobileListCreateView(generics.ListCreateAPIView):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET: Công khai
        # POST: Chỉ admin mới được tạo
        return [IsAdminCustomer()]

class MobileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET: Công khai
        # PUT, PATCH, DELETE: Chỉ admin mới được thực hiện
        return [IsAdminCustomer()]
