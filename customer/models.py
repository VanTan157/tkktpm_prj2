from django.db import models

class Customer(models.Model):
    USER_TYPES = [
        ('user', 'New User'),
        ('admin', 'Admin'),
        ('business', 'Business'),
        ('vip', 'VIP'),
    ]

    customer_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Mã hóa mật khẩu sau
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
    @property
    def is_authenticated(self):
        # Luôn trả về True nếu đã xác thực qua token
        return True
