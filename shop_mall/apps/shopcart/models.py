from django.db import models
from apps.users.models import User
from apps.shops.models import Product
from datetime import datetime
# Create your models here.
class ShoppingCart(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='商品', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='商品数量', default=1)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'tb_cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
