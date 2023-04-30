from django.urls import path
from .views import *

urlpatterns = [
    path('pay/order/create', OrderCreateView.as_view()),
    path('pay/order/show_order', OrderListView.as_view()),
    path('pay/order/', OrderPayView.as_view()),
]
