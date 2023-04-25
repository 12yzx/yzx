from itsdangerous import URLSafeTimedSerializer
from shop_mall import settings


def send_email_token(user_id):
    # 对数据加密的操作以及解密
    s = URLSafeTimedSerializer(secret_key=settings.SECRET_KEY)

    data = s.dumps(user_id)
    return data


def check_email_token(token):
    # 解密
    s = URLSafeTimedSerializer(secret_key=settings.SECRET_KEY)
    try:
        user_id = s.loads(token, max_age=60*60)
    except Exception as e:
        return None

    return user_id
