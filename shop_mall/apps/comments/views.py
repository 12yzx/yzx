from utils.views import LoginRequiredJsonMixin
from .models import ProductComments
from .forms import CommentForm
from apps.shops.models import Product
from django.views import View
from django.http import JsonResponse


