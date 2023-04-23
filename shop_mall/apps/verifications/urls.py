from django.urls import path
from .views import *
urlpatterns = [
   path('image_code/<uuid>', ImageCodeView.as_view()),

]