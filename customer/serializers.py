from rest_framework import serializers
from .models import Customer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password, make_password

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}  # set required=False
        }
    
    def update(self, instance, validated_data):
        # Nếu password có trong validated_data, mã hóa nó trước khi cập nhật
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)



class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Định nghĩa lại các trường input:
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # Gỡ bỏ logic mặc định của TokenObtainPairSerializer
    

    def __init__(self, *args, **kwargs):
        # Gọi khởi tạo của lớp cha
        super().__init__(*args, **kwargs)
        # Sau khi các trường của lớp cha được tạo ra, loại bỏ trường 'username'
        if 'username' in self.fields:
            self.fields.pop('username')
    
    def validate(self, attrs):
        # Lấy email, password từ request
        email = attrs.get('email')
        password = attrs.get('password')

        # Tìm user theo email
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            raise serializers.ValidationError({"email": "Email không tồn tại."})

        if not check_password(password, customer.password):
            raise serializers.ValidationError({"password": "Mật khẩu không chính xác."})

        # Sinh token
        refresh = self.get_token(customer)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data

    @classmethod
    def get_token(cls, user):
        # Gọi super để lấy token, sau đó custom
        token = super().get_token(user)
        token['email'] = user.email
        return token

