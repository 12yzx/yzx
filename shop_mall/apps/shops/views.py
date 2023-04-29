from django.views import View
from models import *
class ShowShopView(View):
    """商品信息"""
    def get(self, request):
        Product.objects.all()