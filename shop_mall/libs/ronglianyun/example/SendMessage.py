from ronglian_sms_sdk import SmsSDK

accId = '2c94811c87a40a620187ac15019d016a'
accToken = 'c8afd58e076047408dd1643a18b45f42'
appId = '2c94811c87a40a620187ac15029a0171'

def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    tid = '容联云通讯创建的模板'
    mobile = '手机号1,手机号2'
    datas = ('变量1', '变量2')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)

send_message()


