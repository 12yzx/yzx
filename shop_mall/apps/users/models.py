from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    default_address = models.ForeignKey('Address', related_name='users',
                                        null=True, blank=True, on_delete=models.SET_NULL,
                                        verbose_name='默认地址')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='addresses', verbose_name='用户信息')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='pro_address',
                                 verbose_name='省级地址')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_address',
                             verbose_name='市地址')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='dis_address',
                                 verbose_name='地区')
    place = models.CharField(max_length=50, verbose_name='地址信息')
    mobile = models.CharField(max_length=11, verbose_name='手机信息')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user

