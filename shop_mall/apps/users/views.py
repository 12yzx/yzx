from django.shortcuts import render
from django.views import View
from .models import User
from django.http import JsonResponse


class UsernameCountView(View):

    def get(self, request, username):

        # 1.接受数据
        pass
        # 2.进行用户名验证过查询是否已存在
        count = User.objects.filter(username=username).count()
        # 3.返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


