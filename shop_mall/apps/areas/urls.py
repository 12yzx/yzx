from django.urls import path
from .views import *
urlpatterns = [
   path('areas/', AreaView.as_view()),
   path('county/<id>', CountyView.as_view())

]
