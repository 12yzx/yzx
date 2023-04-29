from django.contrib.auth.hashers import make_password
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from utils.email_token import send_email_token, check_email_token
from utils.views import LoginRequiredJsonMixin
from django.core.mail import send_mail
from celery_tasks.sned_email.tasks import celery_send_email
from .models import User, Address
from itsdangerous import URLSafeTimedSerializer
from shop_mall import settings
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

    def post(self, request):
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
            return JsonResponse({'code': 400, 'errmsg': '用户已注册'})

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
            return JsonResponse({'code': 400, 'errmsg': '手机号已存在'})
        pattern = r'^1[0-9]{10}$'
        if not re.match(pattern, mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号码不符合要求，应为1开头的十一位'})

        # 4.数据保存
        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        # 状态保持
        login(request, user)

        return JsonResponse({'code': 0, 'errmsg': '首页返回'})


class LoginView(View):
    """
    登录实现
    """
    def post(self, request):
        # 1.接受数据
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        # 是否保持登录状态
        remember = data.get('remember')
        # 2.验证数据
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 用户名或手机号登录的实现
        # if re.match('1[3-9]\d{9}', username):
        #     User.USERNAME_FIELD = 'mobile'
        # else:
        #     User.USERNAME_FIELD = 'username'

        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误'})

        login(request, user)
        # 3.判断是否保持登录
        if remember:
            request.session.set_expiry(60*30)   # 默认是2周
        else:
            request.session.set_expiry(0)

        # 在前端显示用户信息
        response = JsonResponse({'code': 0, 'errmsg': '登录成功'})
        response.set_cookie('username', username)
        return response


class LogoutView(View):
    """
    退出
    """
    def delete(self, request):
        # 删除session信息
        logout(request)
        # 删除cookie信息
        response = JsonResponse({'code': 0, 'errmsg': '退出'})
        response.delete_cookie('username')
        return response


class CenterView(LoginRequiredJsonMixin, View):
    """未登录返回JSON
        用户中心
    """
    def get(self, request):

        info_data = {
            'username': request.user.username,
            'email': request.user.email,
            'mobile': request.user.mobile,
            'email_active': request.user.email_active,
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})


class EmailView(LoginRequiredJsonMixin, View):
    """
    邮件保存 激活
    """
    def put(self, request):
        # 1.接收邮箱
        data = json.loads(request.body.decode())
        email = data.get('email')
        # 2.验证邮箱
        pattern = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return JsonResponse({'code': 400, 'errmsg': '请输入正确的邮箱'})
        # 3.保存邮箱
        user = request.user
        user.email = email
        user.save()
        # 4.发送邮箱激活
        # 对用户id加密
        token = send_email_token(user.id)
        subject = '激活'
        from_email = '15832011554@163.com'
        email_url = "http://127.0.0.1:8000/success/?token=%s" % token
        message = '<a href="%s ">点击激活 %s</a>' % (email_url, email_url)
        recipient_list = ['15832011554@163.com']
        html_message = message
        # celery_send_email.delay(recipient_list=recipient_list, html_message=html_message)
        # celery建议在linux中运行
        send_mail(
            subject=subject,
            message='hello',
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message
        )
        # 5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': '发送成功'})


class SuccessEmail(View):
    """测试激活"""
    def put(self, request):
        # 1.获取数据
        params = request.GET
        token = params.get('token')
        # 2.验证数据
        if token is None:
            return JsonResponse({'code': 400, 'errmsg': '数据不全'})
        # 对user_id解密
        user_id = check_email_token(token)
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '数据不全'})
        # 查询并修改数据
        user = User.objects.get(id=user_id)
        user.email_active = True
        user.save()
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': '激活成功'})


class ForgetPasswordView(View):
    """忘记密码"""

    def get(self, request):
        # 接收请求
        return HttpResponse('返回找回密码界面')

    def post(self, request):
        # 1接收数据
        data = json.loads(request.body.decode())
        email = data.get('email')
        # 2.验证数据
        pattern = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return JsonResponse({'code': 400, 'errmsg': '请输入正确的邮箱'})
        user = User.objects.get(email=email)
        if not user:
            return JsonResponse({'code': 400, 'errmsg': '邮箱未注册'})
        user_id = user.id
        token = send_email_token(user_id)
        subject = '找回密码'
        from_email = '15832011554@163.com'
        email_url = "http://127.0.0.1:8000/new_password/?token=%s" % token
        message = '<a href="%s ">点击下面链接找回密码 %s</a>' % (email_url, email_url)
        recipient_list = ['15832011554@163.com']
        html_message = message
        send_mail(
            subject=subject,
            message='hello',
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message
        )
        return JsonResponse({'code': 0, 'errmsg': 'OK'})


class NewPasswordView(View):
    """修改密码"""
    def put(self, request):
        # 1.获取数据
        params = request.GET
        token = params.get('token')
        data = json.loads(request.body.decode())
        new_password = data.get('new_password')
        # 2.验证数据
        if token is None:
            return JsonResponse({'code': 400, 'errmsg': '数据不全'})
        # 对user_id解密
        user_id = check_email_token(token)
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '数据不全'})
        pattern = r'^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[@$!%*#?&])[a-zA-Z0-9@$!%*#?&]{8,20}$'
        # 密码包含数字、字母和特殊字符，长度为8-20个字符
        if not re.match(pattern, new_password):
            return JsonResponse({'code': 400, 'errmsg': '密码不符合要求'})
        if User.objects.get(id=user_id).password == new_password:
            return JsonResponse({'code': 400, 'errmsg': '新密码不能与旧密码相同'})
        # 查询并修改数据
        user = User.objects.get(id=user_id)
        user.password = make_password(new_password)
        user.save()
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': '密码修改成功'})




class AddressCreateView(LoginRequiredJsonMixin, View):
    """新增地址信息"""
    def post(self, request):
        # 1.获取数据
        date = json.loads(request.body.decode())
        # 2.校验数据
        receiver = date.get('receiver')
        province_id = date.get('province_id')
        city_id = date.get('city_id')
        district_id = date.get('district_id')
        place = date.get('place')
        mobile = date.get('mobile')
        email = date.get('email')
        user = request.user
        if not all([receiver, province_id, city_id, district_id, place, mobile, email]):
            return JsonResponse({'code': 400, 'err,sg': '数据不全'})
        pattern = r'^1[0-9]{10}$'
        if not re.match(pattern, mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号码不符合要求，应为1开头的十一位'})
        pattern = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return JsonResponse({'code': 400, 'errmsg': '请输入正确的邮箱'})
        # 3.保存数据
        address = Address.objects.create(
            user=user,
            receiver=receiver,
            province_id=province_id,
            title=receiver,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            email=email
        )
        address_dict = {
            'id': address.id,
            'title': address.title,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'email': address.email
        }
        # 4.返回数据
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address_dict': address_dict})


class AddressShowView(LoginRequiredJsonMixin, View):
    """页面显示地址信息"""
    def get(self, request):
        # 获取数据
        user = request.user
        addresses = Address.objects.filter(user=user)
        addresses_list = []
        for item in addresses:
            addresses_list.append({
                'id': item.id,
                'title': item.title,
                'receiver': item.receiver,
                'province': item.province.name,
                'city': item.city.name,
                'district': item.district.name,
                'place': item.place,
                'mobile': item.mobile,
                'email': item.email
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses_list': addresses_list})


class AddressUpdateView(LoginRequiredJsonMixin, View):
    """修改信息"""
    def put(self, request, id):
        # 1.获取数据
        date = json.loads(request.body.decode())
        # 2.校验数据
        receiver = date.get('receiver')
        province_id = date.get('province_id')
        city_id = date.get('city_id')
        district_id = date.get('district_id')
        place = date.get('place')
        mobile = date.get('mobile')
        email = date.get('email')
        pattern = r'^1[0-9]{10}$'
        if not re.match(pattern, mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号码不符合要求，应为1开头的十一位'})
        pattern = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return JsonResponse({'code': 400, 'errmsg': '请输入正确的邮箱'})
        address_update = Address.objects.filter(id=id).update(
            receiver=receiver,
            province=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            email=email
        )
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address_update': address_update})


class AddressDeleteView(LoginRequiredJsonMixin, View):
    """删除地址信息"""

    def delete(self, request, id):
        # 1.获取删除对象
        address_delete = Address.objects.filter(id=id)
        # 逻辑删除
        address_delete.update(
            is_delete=True
        )
        # 物理删除
        # address_delete.delete()
        # 2.返回响应
        return JsonResponse({'code': 0, "errmsg": '删除成功'})












