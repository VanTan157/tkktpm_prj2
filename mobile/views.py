from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Mobile
from .serializers import MobileSerializer
from customer.permissions import IsAdminCustomer# Custom permission đã định nghĩa
from bson import ObjectId

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

    lookup_field = '_id'  # Dùng '_id' thay vì 'pk'

    def get_object(self):
        # Lấy giá trị _id từ URL (dạng chuỗi)
        lookup_value = self.kwargs[self.lookup_field]
        # Chuyển thành ObjectId
        obj_id = ObjectId(lookup_value)
        # Truy vấn với _id là ObjectId
        obj = self.get_queryset().get(_id=obj_id)
        return obj

    def get_permissions(self):
        mobile = Mobile.objects.get(_id=ObjectId("67bdf5c99a03c89dd9bfb763"))
        print(mobile.name)
        if self.request.method == 'GET':
            return [AllowAny()]  # GET: Công khai
        # PUT, PATCH, DELETE: Chỉ admin mới được thực hiện
        return [IsAdminCustomer()]