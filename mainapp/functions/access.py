__author__ = 'gaoxindai'

from mainapp.models import user_session
from mainapp.static import constant
import datetime
import urllib2
import json


class Access(object):

    def __init__(self):
        pass

    def record_session_Id(self, fb_id, session_id, issued_time, expire_time):
        user_session(
            fb_id=fb_id,
            session_id=session_id,
            issued_time=issued_time,
            expire_time=expire_time,
        ).save()
        return True

    def check_session_Id(self, fb_id, session_id):
        user_session_obj = user_session.objects.get(fb_id=fb_id)
        db_session_id = user_session_obj.session_id
        db_expire_time = user_session_obj.expire_time
        today = datetime.datetime.now()
        if session_id == db_session_id and db_expire_time.date() > today.date():
            return 0
        else:
            return 1

    def update_session_Id(self, fb_id, session_id, issued_time, expire_time):
        user_session_obj = user_session.objects.get(fB_id=fb_id)
        user_session_obj.session_id = session_id
        user_session_obj.issued_time = issued_time
        user_session_obj.expire_time = expire_time
        user_session_obj.save()
        return True

    def get_access_token(self):
        access_token_url = constant.get_access_token_api
        req_access = urllib2.Request(access_token_url)
        res_access = urllib2.urlopen(req_access)
        data_access = res_access.read()
        access_token = data_access[13:]
        return access_token

    def get_token_info(self, input_token, access_token):
        validate_token_url = constant.validate_fb_token_api % (input_token, access_token)
        req_validate = urllib2.Request(validate_token_url)
        res_validate = urllib2.urlopen(req_validate)
        data_validate = res_validate.read()
        data_validate = json.loads(data_validate)
        is_valid = data_validate["data"]["is_valid"]
        if is_valid:
            expire_time = datetime.datetime.fromtimestamp(data_validate["data"]["expires_at"])
            issued_time = datetime.datetime.fromtimestamp(data_validate["data"]["issued_at"])
            session_fb_id = data_validate["data"]["user_id"]
            data = dict(
                is_valid=is_valid,
                expire_time=expire_time,
                issued_time=issued_time,
                session_fb_id=session_fb_id
            )
            return data
        else:
            return False

    def check_access(self, fb_id, session_id):
        access_token = self.get_access_token()
        try:
            user_session_obj = user_session.objects.get(fb_id=fb_id)
            expire_time = user_session_obj.expire_time
            if expire_time.date() < datetime.datetime.today().date():
                session_info = self.get_token_info(session_id, access_token)
                if session_info:
                    session_fb_id = session_info["session_fb_id"]
                    if session_fb_id == fb_id:
                        expire_time = session_info["expire_time"]
                        issued_time = session_info["issued_time"]
                        self.update_session_Id(fb_id, session_id, issued_time, expire_time)
                        status_code = 0
                    else:
                        status_code = 1
                else:
                    status_code = 1
            else:
                status_code = self.check_session_Id(fb_id, session_id)
        except user_session.DoesNotExist:
            session_info = self.get_token_info(session_id, access_token)
            if session_info:
                session_fb_id = session_info["session_fb_id"]
                if session_fb_id == fb_id:
                    expire_time = session_info["expire_time"]
                    issued_time = session_info["issued_time"]
                    self.record_session_Id(fb_id, session_id, issued_time, expire_time)
                    status_code = 0
                else:
                    status_code = 1
            else:
                status_code = 1
        return status_code