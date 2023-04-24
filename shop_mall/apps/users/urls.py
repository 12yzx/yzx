from django.urls import path
from .views import *
urlpatterns = [
    path('usernames/<username:username>', UsernameCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('center/', CenterView.as_view()),

]
