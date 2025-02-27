from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cart
from mobile.models import Mobile
from .serializers import CartSerializer
from decimal import Decimal
from bson import ObjectId

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.using('postgresql').all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Tính total_price từ mobile_id
        items = serializer.validated_data.get('items', [])
        total_price = Decimal('0.00')
        mobile = Mobile.objects.using('mongodb').filter(_id="67c08abd41bf0c095d48c858").first()
        print(mobile)
        if items:
            items = [ObjectId(item) for item in items]
            mobiles = Mobile.objects.using('mongodb').filter(_id__in=items)
            total_price = sum(Decimal(str(mobile.price)) for mobile in mobiles)

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
            mobiles = Mobile.objects.using('mongodb').filter(_id__in=items)
            total_price = sum(Decimal(str(mobile.price)) for mobile in mobiles)

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)