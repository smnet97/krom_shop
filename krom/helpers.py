import requests
import time
from django.conf import settings
import random

# from django.contrib.sites import requests

from user.models import SmsCode, SmsAttempt
from datetime import datetime, timedelta
from django.core.exceptions import SuspiciousOperation
from django.db.models import F


def sms_code():
    return str(random.randint(100000, 999999))


def send_sms_code(request, phone):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    ip_count = SmsCode.objects.filter(ip=ip).count()
    if ip_count > 1000:
        raise SuspiciousOperation("Over limit")

    phone_count = SmsCode.objects.filter(phone=phone).count()
    if phone_count > 1000:
        raise SuspiciousOperation("Over limit")

    code = sms_code()

    model = SmsCode()
    model.ip = ip
    model.phone = phone
    model.code = code
    model.expire_at = datetime.now() + timedelta(minutes=10)
    model.save()

    send_sms(phone, "Tasdiqlash kodi " + code)
    return code


def validate_sms_code(phone, code):
    try:
        obj = SmsAttempt.objects.get(phone=phone)
        if obj.counter >= 1000:
            return False


        obj.counter = F('counter') + 1
    except SmsAttempt.DoesNotExist:
        obj = SmsAttempt(phone=phone, counter=1)

    obj.last_attempt_at = datetime.now()
    obj.save()

    codes = SmsCode.objects.filter(phone=phone, expire_at__gt=datetime.now()).all()

    for row in codes:
        if row.code == code:
            return True

    return False


def send_sms(phone, text):


    try:
        r = requests.post("http://91.204.239.44/broker-api/send", json={
            'messages': [
                {
                    'recipient': phone,
                    'message-id': 'krom' + str(round(time.time() * 1000)),
                    'sms': {
                        'originator': 'NAPA',
                        'content': {
                            'text': text,
                        }
                    }

                }
            ]
        }, auth=(settings.SMS_USERNAME, settings.SMS_PASSWORD))
        print(r.text)
    except Exception as e:
        print(e)
        return False

    return True
