from django.views import View
from utils.views import LoginRequiredJsonMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from apps.shops.models import Product
from .models import ShoppingCart
from django.core.cache import cache
# Create your views here.

class ShopCartView(LoginRequiredJsonMixin, View):
    """添加购物车"""
    def post(self, request, pro_id):
        # 获取用户信息
        user = request.user
        # 查询商品信息
        product = get_object_or_404(Product, id=pro_id)
        # 判断是否存在
        if ShoppingCart.objects.filter(user=user, product=product).exists():
            # 更新数量
            cart = ShoppingCart.objects.get(user=user, product=product)
            if cart.num < product.num:
                cart.num += 1
            else:
                raise Exception('超出商品最大数量')

            cart.save()
        else:
            # 添加新的购物车商品
            cart = ShoppingCart(user=user, product=product, num=1)
            cart.save()

        return JsonResponse({'code': 0, 'msg': '商品成功添加到购物车！'})


class CartListView(LoginRequiredJsonMixin, View):
    def get(self, request):
        # 获取用户信息
        user = request.user

        # 查询购物车中的商品
        cart_items = ShoppingCart.objects.filter(user=user)
        cart_list = []
        for item in cart_items:
            cart_list.append({
                'id': item.id,
                'product_id': item.product.id,
                'product_name': item.product.name,
                'product_price': item.product.price,
                'product_num': item.num,
                'product_image': item.product.mainimg.url
            })
        # 缓存redis中
        cache.set('cart_list', cart_list, 24*3600)
        return JsonResponse({'code': 0, 'cart_list': cart_list})


class DeleteCartInfoView(LoginRequiredJsonMixin, View):
    """删除购物车内容"""
    def delete(self, request, cart_id):
        # 获取用户信息
        user = request.user

        # 查询购物车信息
        cart_item = get_object_or_404(ShoppingCart, id=cart_id, user=user)

        # 删除商品
        cart_item.delete()
        return JsonResponse({'code': 0, 'msg': '删除成功'})

