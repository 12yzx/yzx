from django.core.mail import send_mail
from celery_tasks.main import app

@app.task
def celery_send_email(recipient_list,  html_message):
    subject = '激活'
    from_email = '15832011554@163.com'

    send_mail(
        subject=subject,
        message='hello',
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message
    )