from django.views import View
from .models import *
from django.http import JsonResponse
from django.db.models import Q
import json


class ShowShopView(View):
    """商品信息"""
    def get(self, request):
        # 1.获取数据
        date = json.loads(request.body.decode())
        all_pros = Product.objects.all().order_by('-add_time')
        pro_type = date.get('pro_type')
        if pro_type:
            all_pros = Product.objects.filter(pro_type=pro_type)
        info_list = []
        for info in all_pros:
            info_list.append({
                'name': info.name,
                'price': info.price,
            })

        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': '查询成功', 'info_list': info_list})


class ShopInfoView(View):
    """商品详情页"""
    def get(self, request, pro_id):
        # # 1.获取数据
        if not pro_id:
            return JsonResponse({'code': 400, 'errmsg': '商品不存在'})
        product = Product.objects.get(id=pro_id)
        images = product.img.all()
        # 构建图片信息列表
        image_list = []
        for img in images:
            image_list.append({
                'url': img.image.url,  # 获取图片的 URL
                'width': img.image.width,  # 获取图片宽度
                'height': img.image.height,  # 获取图片高度
            })

        # 构建商品信息字典，包含图片信息列表
        product_info = {
            'name': product.name,
            'price': product.price,
            'num': product.num,
            'freight': product.freight,
            'origin': product.origin,
            'images': image_list,  # 包含图片信息列表
        }

        # 将商品信息字典转为 JSON 格式
        product_info_json = json.dumps(product_info)
        # 返回 JSON 格式数据
        return JsonResponse({'code': 0, 'product_info': product_info_json})


class SearchView(View):
    """实现全局搜索"""
    def get(self, request):
        query = request.GET.get('q', '')  # 获取搜索关键字
        if not query:
            return JsonResponse({'results': []})

        products = Product.objects.filter(Q(name__icontains=query) | Q(details__icontains=query))  # 搜索相关记录

        results = []
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'details': product.details,
                'price': product.price,
            })

        return JsonResponse({'results': results})


