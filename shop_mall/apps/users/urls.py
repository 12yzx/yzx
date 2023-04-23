from django.urls import path
from .views import *
urlpatterns = [
    path('usernames/<username:username>', UsernameCountView.as_view()),
    path('register/', RegisterView.as_view()),

]
