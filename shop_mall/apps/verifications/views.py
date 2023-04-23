from django.http import HttpResponse
from django.views import View
from captcha.image import ImageCaptcha
from django_redis import get_redis_connection
from django.http import JsonResponse
from random import randint

from libs.ronglianyun.example.SendMessage import send_message


class ImageCodeView(View):

    def get(self, request, uuid):
        """
        实现图形验证码逻辑
        :param uuid: UUID
        :return: image/jpg
        """
        # 生成图形验证码
        # text：验证码； image：验证码的图形（字节数据）
        image = ImageCaptcha()
        text = image.generate(str(uuid))

        # 保存图形验证码
        # 使用配置的redis数据库的别名，创建连接到redis的对象
        redis_conn = get_redis_connection('code')
        # 使用连接到redis的对象去操作数据存储到redis
        # 图形验证码必须要有有效期的：设计是300秒有效期
        text = text.getvalue()
        redis_conn.setex(uuid, 300, text)

        # 响应图形验证码: image/jpg

        return HttpResponse(image, content_type='image/jpg')

class SmsCodeView(View):

    def get(self, request, mobile):
        # 1.获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2.校验参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '数据不全'})
        # 3.链接redis
        redis_conn = get_redis_connection('code')
        # 获取redis数据
        redis_image_code = redis_conn.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证已过期'})
        # 生成短信验证码
        sms_code = '%06d' % randint(0, 999999)
        # 接收标记查看是否存在 避免频繁发送
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag is not None:
            return JsonResponse({'code': 400, 'errmsg': '频繁发送'})

        # 使用管道提升redis性能
        pipe = redis_conn.pipeline()
        #  保存验证码
        pipe.setex(mobile, 300, sms_code)
        # 添加有效期标志
        pipe.setex('send_flag_%s' % mobile, 60, 1)
        pipe.execute()

        # 5.发送
        send_message(1 ,mobile, (sms_code, "5"))

        return JsonResponse({'code': '0', 'errmsg': '发送成功'})









