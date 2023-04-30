from django.db import models
from apps.users.models import User
from apps.shops.models import Product

# Create your models here.
class ProductComments(models.Model):
    user = models.ForeignKey(User, verbose_name='下单用户', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='商品', on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name='评论内容')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        db_table = 'tb_comments'
        verbose_name = '商品评论'
        verbose_name_plural = verbose_name
