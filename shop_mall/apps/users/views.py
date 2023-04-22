from django.shortcuts import render
from django.views import View
from .models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login
import re
import json


class UsernameCountView(View):

    def get(self, request, username):
        # 1.接受数据并进行判断
        # if not re.match('[a-zA-Z0-9_-]{5,20}', username):
        #     return JsonResponse({'code': 200, 'errmsg': '用户名不满足需求'})
        # 2.进行用户名验证过查询是否已存在
        count = User.objects.filter(username=username).count()
        # 3.返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class RegisterView(View):

    def get(self, request):

        # 获取请求后返回注册页面
        return HttpResponse('200 ok')

    def post(self,request):
        # 接收请求
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)

        # 2. 获取字典中数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')

        # 3. 验证数据

        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '数据不全'})

        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})

        # if not re.match('[]'):
        #     pass

        # 4.数据保存
        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        # 状态保持
        login(request, user)

        return JsonResponse({'code': 0, 'errmsg': '首页返回'})





