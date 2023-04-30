from django.urls import path
from .views import *

urlpatterns = [
   path('show_info/', ShowShopView.as_view()),
   path('detail_info/<int:pro_id>', ShopInfoView.as_view()),
]
