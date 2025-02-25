from djongo import models  # Sử dụng models của djongo thay vì django.db.models

class Mobile(models.Model):
    # Trường _id mặc định của MongoDB, sử dụng ObjectIdField làm khóa chính.
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='mobiles/', blank=True, null=True)

    def __str__(self):
        return self.name
