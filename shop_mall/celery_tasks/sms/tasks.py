# 设置执行任务
from libs.ronglianyun.example import SendMessage
from celery_tasks.main import app


@app.task
def celery_send_msg(mobile, code):

    SendMessage.send_message(mobile, [code, 5])
