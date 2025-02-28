from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cart
from mobile.models import Mobile
from .serializers import CartSerializer
from decimal import Decimal
from bson import ObjectId
from rest_framework.permissions import IsAuthenticated
from customer.permissions import IsAdminCustomer  # Import permission đã định nghĩa
from customer.authentication import CustomerJWTAuthentication

class CartViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomerJWTAuthentication]  # Sử dụng JWT tùy chỉnh
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.using('postgresql').all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Tính total_price từ items
        items = serializer.validated_data.get('items', [])
        total_price = Decimal('0.00')
        if items:
            mobile_ids = [ObjectId(item['mobile_id']) for item in items]
            mobiles = Mobile.objects.using('mongodb').filter(_id__in=mobile_ids)
            # Tạo dictionary để tra cứu mobile theo _id
            mobile_dict = {str(mobile._id): mobile for mobile in mobiles}
            # Tính tổng giá dựa trên price và quantity
            total_price = sum(
                Decimal(str(mobile_dict[item['mobile_id']].price)) * Decimal(item['quantity'])
                for item in items
                if item['mobile_id'] in mobile_dict
            )

        serializer.validated_data['total_price'] = total_price
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Tính lại total_price nếu items thay đổi
        items = serializer.validated_data.get('items', instance.items)
        total_price = Decimal('0.00')
        if items:
            mobile_ids = [ObjectId(item['mobile_id']) for item in items]
            mobiles = Mobile.objects.using('mongodb').filter(_id__in=mobile_ids)
            mobile_dict = {str(mobile._id): mobile for mobile in mobiles}
            total_price = sum(
                Decimal(str(mobile_dict[item['mobile_id']].price)) * Decimal(item['quantity'])
                for item in items
                if item['mobile_id'] in mobile_dict
            )

        serializer.validated_data['total_price'] = total_price
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete(using='postgresql')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        print(f"User: {request.user}, Is Admin: {getattr(request.user, 'customer_type', None) == 'admin'}")
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        is_admin = getattr(user, 'customer_type', None) == 'admin'
        if is_admin:
            customer_id = request.query_params.get('customer_id', None)
            if customer_id is not None:
                try:
                    customer_id = int(customer_id)
                    queryset = queryset.filter(customer_id=customer_id)
                except ValueError:
                    return Response({"detail": "customer_id phải là một số nguyên."}, status=400)
        else:
            queryset = queryset.filter(customer_id=user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)