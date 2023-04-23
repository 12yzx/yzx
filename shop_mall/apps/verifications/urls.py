from .views import ImageCodeView, SmsCodeView
from django.urls import path
urlpatterns = [
    path('image_codes/<uuid>', ImageCodeView.as_view()),
    path('sms_code/<mobile>', SmsCodeView.as_view()),
]

