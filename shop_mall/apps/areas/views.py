from django.shortcuts import render
from django.views import View
from apps.areas.models import Area
from django.http import JsonResponse
from django.core.cache import cache


class AreaView(View):
    """
    省市区信息获取
    """
    def get(self, request):
        # 1.查询省级市县 并处理信息
        province_list = cache.get('provinces')
        if province_list is None:
            provinces = Area.objects.filter(parent=None)
            province_list = []
            for province in provinces:
                province_list.append({
                    'id': province.id,
                    'name': province.name
                }
                )
            # 进行缓存 减少数据库查询
            cache.set('provinces', province_list, 24*3600)

        # 2.返回响应
        return JsonResponse({'code': 0, 'errmsg': '查询成功', 'province_list': province_list})


class CountyView(View):
    """获取市县的信息"""
    def get(self, request, id):
        # 1.获取数据
        down_level_list = cache.get('cities_list')
        counties_list = cache.get('counties_list')
        provinces = Area.objects.get(id=id)
        if down_level_list is None:
            cities = provinces.subs.all()
            # 数据处理
            down_level_list = []
            for down_level in cities:
                down_level_list.append({
                    'id': down_level.id,
                    'name': down_level.name
                })

            cache.set('cities_list', down_level_list, 24*3600)
        if counties_list is None:
            cities = provinces.subs.all()
            counties = Area.objects.filter(parent__in=cities)
            counties_list = []
            for count_level in counties:
                counties_list.append({
                    'id': count_level.id,
                    'name': count_level.name
                })
            cache.set('counties_list', counties_list, 24*3600)
        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': '查询成功',
                             'down_level_list': down_level_list,
                             'counties_list': counties_list})
