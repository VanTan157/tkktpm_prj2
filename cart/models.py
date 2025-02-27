from django.db import models

class Cart(models.Model):
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    items = models.JSONField(
        default=list,  # Danh sách các mobile_id
        help_text="Danh sách các mobile_id từ MongoDB"
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Giỏ hàng của {self.customer_name}"

    class Meta:
        db_table = 'cart'