from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField


class Product(models.Model):
    """
    商品信息
    """
    name = models.CharField(max_length=30, verbose_name='商品名称')
    price = models.FloatField(verbose_name='单价')
    num = models.IntegerField(verbose_name='数量')
    freight = models.IntegerField(verbose_name='运费', default=0)
    origin = models.CharField(max_length=20, verbose_name='产地')
    pro_type = models.CharField(max_length=3, choices=(('ncp', '农产品'),
                                                       ('sg', '水果'),
                                                       ('ls', '零食')
                                                       ),
                                verbose_name='分类', default='ls')
    buyers = models.IntegerField(default=0, verbose_name='购买人数')
    comments = models.IntegerField(default=0, verbose_name='评论人数')
    details = RichTextField()
    mainimg = models.ImageField(upload_to='product/img/%Y/%m', default='', verbose_name='商品主图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'tb_product'
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name
        app_label = 'shops'

    def __str__(self):
        return self.name


class ProPic(models.Model):
    product = models.ForeignKey(Product, related_name='img', verbose_name='商品', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m', verbose_name='商品图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'tb_img'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name
        app_label = 'shops'
