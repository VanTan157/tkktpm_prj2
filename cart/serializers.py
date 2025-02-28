from bson import ObjectId
from rest_framework import serializers
from .models import Cart
from customer.models import Customer
from mobile.models import Mobile

class CartSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    items = serializers.JSONField()  # Vẫn là JSONField, nhưng chứa danh sách các object

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
            # Kiểm tra xem item có phải là dict và có các trường cần thiết không
            if not isinstance(item, dict) or 'mobile_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Mỗi item phải là một object chứa 'mobile_id' và 'quantity'.")
            
            mobile_id = item['mobile_id']
            quantity = item['quantity']

            # Kiểm tra mobile_id
            if not isinstance(mobile_id, str):
                raise serializers.ValidationError("mobile_id phải là một chuỗi.")
            try:
                mobile_id_obj = ObjectId(mobile_id)
                if not Mobile.objects.using('mongodb').filter(_id=mobile_id_obj).exists():
                    raise serializers.ValidationError(f"Mobile với ID {mobile_id} không tồn tại.")
            except ValueError:
                raise serializers.ValidationError(f"ID {mobile_id} không phải là ObjectId hợp lệ.")

            # Kiểm tra quantity
            if not isinstance(quantity, int) or quantity <= 0:
                raise serializers.ValidationError("quantity phải là một số nguyên dương.")

        return value