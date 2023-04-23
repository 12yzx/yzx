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
        # 判断是否已存在
        if User.objects.filter(username=username):
            return JsonResponse({'code': '400', 'errmsg': '用户已注册'})

        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '数据不全'})

        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})

        # 密码包含数字、字母和特殊字符，长度为8-20个字符
        pattern = r'^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[@$!%*#?&])[a-zA-Z0-9@$!%*#?&]{8,20}$'
        if not re.match(pattern, password):
            return JsonResponse({'code': 400, 'errmsg': '密码不符合要求'})

        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码不一致'})

        # 判断手机号是否存在以及是否符合要求
        if User.objects.filter(mobile=mobile):
            return JsonResponse({'code': '400', 'errmsg': '手机号已存在'})
        pattern = r'^1[0-9]{10}$'
        if not re.match(pattern, mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号码不符合要求，应为1开头的十一位'})

        # 4.数据保存
        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        # 状态保持
        login(request, user)

        return JsonResponse({'code': 0, 'errmsg': '首页返回'})





