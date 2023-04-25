from django.db import models

# Create your models here.
class Area(models.Model):

    name = models.CharField(max_length=20, verbose_name='地区名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='subs',
                               null=True,
                               verbose_name='省市区上级')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

