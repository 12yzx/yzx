from django.urls import path
from .views import *
urlpatterns = [
    path('add_cart/<int:pro_id>', ShopCartView.as_view()),
    path('show_cart/', CartListView.as_view()),
    path('delete_cart/<int:cart_id>', DeleteCartInfoView.as_view())

]
