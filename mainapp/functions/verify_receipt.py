__author__ = 'gaoxindai'

from mainapp.static import constant
from mainapp.models import user_transaction
import urllib2
import json
import datetime


class VerifyReceipt():

    def __init__(self):
        pass

    def verify_receipt(self, user_fb_id, receipt_data):
        transaction_id_list = []
        validate_receipt_api = constant.validate_receipt_api
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        data = {"receipt-data": receipt_data}
        data = json.dumps(data)
        req = urllib2.Request(validate_receipt_api, data, headers)
        res = urllib2.urlopen(req)
        receipt_info_json = res.read()
        receipt_info = json.loads(receipt_info_json)
        status = receipt_info["status"]
        if not status:
            for item in receipt_info["receipt"]["in_app"]:
                purchase_date_epoch = int(item['purchase_date_ms'][0:10])
                purchase_date = datetime.datetime.fromtimestamp(purchase_date_epoch)
                print purchase_date
                transaction_id_list.append(dict(
                    transaction_id=item["transaction_id"],
                    purchase_date=purchase_date
                ))
            transaction_data = dict(
                user_fb_id=user_fb_id,
                transaction_id_list=transaction_id_list,
            )
        else:
            transaction_data = 0
        return transaction_data

    def record_transaction(self, user_fb_id, transaction_id, purchase_date):
        user_transaction(
            user_fb_id=user_fb_id,
            transaction_id=transaction_id,
            purchase_date=purchase_date,
        ).save()
        return 0

    def check_purchase(self, user_fb_id, receipt_data, status_code):
        transaction_data = self.verify_receipt(user_fb_id, receipt_data)
        if transaction_data:
            user_fb_id = transaction_data["user_fb_id"]
            transaction_id_list = transaction_data["transaction_id_list"]
            for item in transaction_id_list:
                transaction_id = item["transaction_id"]
                purchase_date = item["purchase_date"]
                try:
                    user_transaction.objects.get(transaction_id=transaction_id)
                    status_code = 4
                    break
                except user_transaction.DoesNotExist:
                    print user_fb_id, transaction_id, purchase_date
                    self.record_transaction(user_fb_id, transaction_id, purchase_date)
        else:
            status_code = 5
        return status_code


