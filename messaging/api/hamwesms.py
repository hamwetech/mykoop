import json
import requests
import logging
import traceback
from django.conf import settings
from conf.utils import log_debug, log_error


class MessagingOperations():

    def __init__(self):
        self.password = 'IvJhk4THhCMPBkjfC8R4'
        self.user = 'admin'

    def sendOneSMS(self, msisdn, message):
        data = {
            'token': self.password,
            'purpose': 'BULKSMS',
            'message': message,
            'msisdn': msisdn
        }

        return self.sendRequest(data)

    def sendRequest(self, params):
        try:
            log_debug('Message Sent: %s' % params)
            url = self.getApiHost()
            r = requests.get(url, params=params, verify=False)
            log_debug('Message Response: %s' % r.text)
            return json.loads(r.text)
        except Exception as e:
            log_error()
            return {"status": "failed", "response": "Error Message: %s" % e}

    def getApiHost(self):
        return "https://sms.hamwe.org/bsapirq/"

    def send_message(self, msisdn, message):
        send_status = True
        if send_status:
            res = self.sendOneSMS(msisdn, message)
            status = 'SUCCESS' if res['status'].lower() == 'ok' else 'FAILED'
            return status