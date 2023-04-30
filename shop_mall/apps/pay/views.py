from django.views import View
from django.http import JsonResponse
from apps.shops.models import Product
from .models import Order
from . import payment

class OrderCreateView(View):
    """创建订单"""
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('num')
        if not product_id or not quantity:
            return JsonResponse({'code': 400, 'error': '参数不全'})

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': '商品不存在'})

        try:
            quantity = int(quantity)
        except ValueError:
            return JsonResponse({'error': '数量必须为整数'})

        if quantity < 1:
            return JsonResponse({'error': '数量必须大于等于1'})

        total_price = product.price * quantity

        order = Order.objects.create(
            product_id=product.id,
            num=quantity,
            total_price=total_price
        )

        return JsonResponse({'order_id': order.id})


class OrderListView(View):
    """订单列表显示"""
    def get(self, request):
        orders = Order.objects.all().select_related('product')
        orders_list = []
        for order in orders:
            orders_list.append({
                'id': order.id,
                'product_id': order.product.id,
                'product_name': order.product.name,
                'quantity': order.num,
                'total_price': order.total_price,
                'created_at': order.created_at
            })
        return JsonResponse({'orders': orders_list})


class OrderPayView(View):
    def post(self, request):
        order_id = request.POST.get('order_id')
        if not order_id:
            return JsonResponse({'error': 'order_id is required'})

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': '订单不存在'})
        # 测试支付，具体需要根据sdk实现
        payment_url = payment.get_payment_url(order.total_price)

        return JsonResponse({'payment_url': payment_url})
