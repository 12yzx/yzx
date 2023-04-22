from django.urls import path
from .views import UsernameCountView
urlpatterns = [
    path('usernames/<username>', UsernameCountView.as_view())
]
