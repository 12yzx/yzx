from django.db import models
from apps.shops.models import Product
# Create your models here.
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    num = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_pay'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
