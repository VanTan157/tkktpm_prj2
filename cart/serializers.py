from bson import ObjectId
from rest_framework import serializers
from .models import Cart
from customer.models import Customer
from mobile.models import Mobile

class CartSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    items = serializers.JSONField()

    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'customer_name', 'phone_number', 'address', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'total_price']

    def validate_customer_id(self, value):
        # Kiểm tra xem customer_id có tồn tại trong MySQL không
        if not Customer.objects.using('mysql').filter(id=value).exists():
            raise serializers.ValidationError(f"Customer với ID {value} không tồn tại.")
        return value
    
    def validate_items(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Items phải là một danh sách.")
        for item in value:
            if not isinstance(item, str):
                raise serializers.ValidationError("Mỗi item phải là một chuỗi mobile_id.")
            try:
                # Chuyển đổi chuỗi thành ObjectId
                mobile_id = ObjectId(item)
                if not Mobile.objects.using('mongodb').filter(_id=mobile_id).exists():
                    raise serializers.ValidationError(f"Mobile với ID {item} không tồn tại.")
            except ValueError:
                raise serializers.ValidationError(f"ID {item} không phải là ObjectId hợp lệ.")
        return value