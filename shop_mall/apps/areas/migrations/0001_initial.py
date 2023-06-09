# Generated by Django 4.2 on 2023-04-25 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='地区名称')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='areas.area', verbose_name='省市区上级')),
            ],
            options={
                'verbose_name': '省市区',
                'verbose_name_plural': '省市区',
                'db_table': 'tb_areas',
            },
        ),
    ]
