import alipay
# 测试支付
def get_payment_url(total_price):
    client = alipay.AliPay(
        appid='your_appid',
        app_notify_url='your_notify_url',
    )

    order_string = client.api_alipay_trade_page_pay(
        out_trade_no='your_out_trade_no',
        total_amount=total_price,
        subject='your_subject',
        return_url='your_return_url',
    )

    return f'https://openapi.alipay.com/gateway.do?{order_string}'
