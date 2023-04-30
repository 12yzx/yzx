from django.urls import path
from .views import *
urlpatterns = [
    path('comments/<int:product_id>', CommentListView.as_view(), name='comment_list'),
    path('comment/<int:product_id>', CommentCreateView.as_view(), name='comment_create'),

]
