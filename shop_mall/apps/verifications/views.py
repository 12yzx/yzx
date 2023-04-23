from django.shortcuts import render
from django.views import View



class ImageCodeView(View):

    def get(self, request, uuid):
        # 1.接收uuid
        # 2.生成图片验证， 图片二进制

        # 3.保存在redis
        # 4.返回结果图片二进制
        pass

