# Generated by Django 4.2 on 2023-04-30 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_alter_propic_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propic',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='img', to='shops.product', verbose_name='商品'),
        ),
    ]