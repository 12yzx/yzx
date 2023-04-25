from celery import Celery
import os
# 加载在django中的环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_mall.settings')

# 1.创建celery实例对象
app = Celery('celery_tasks')

# 2.加载消息队列
app.config_from_object('celery_tasks.broker_config')

# 3.自动识别任务
app.autodiscover_tasks('celery_tasks.sms', 'celery_tasks.send_mail')

