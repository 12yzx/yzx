from django.shortcuts import render
from django.views import View
from apps.areas.models import Area
from django.http import JsonResponse


class AreaView(View):
    """
    省市区信息获取
    """
    def get(self, request):
        # 1.查询省级市县 并处理信息
        provinces = Area.objects.filter(parent=None)

        province_list = []
        for province in provinces:
            province_list.append({
                'id': province.id,
                'name': province.name
            }
            )

        # 2.返回响应
        return JsonResponse({'code': 0, 'errmsg': '查询成功', 'province_list': province_list})


class CountyView(View):
    """获取市县的信息"""
    def get(self, request, id):
        # 1.获取数据
        provinces = Area.objects.get(id=id)
        cities = provinces.subs.all()
        counties = Area.objects.filter(parent__in=cities)
        # 数据处理
        down_level_list = []
        for down_level in cities:
            down_level_list.append({
                'id': down_level.id,
                'name': down_level.name
            })
        counties_list = []
        for count_level in counties:
            counties_list.append({
                'id': count_level.id,
                'name': count_level.name
            })

        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': '查询成功',
                             'down_level_list': down_level_list,
                             'counties_list': counties_list})
