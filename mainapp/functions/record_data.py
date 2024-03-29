__author__ = 'gaoxindai'

from mainapp.models import user
from mainapp.models import user_rating
from mainapp.models import user_exception
from mainapp.models import user_info
from django.db.models import F


class RecordData(object):

    def __init__(self):
        self.ratio = 0.1

    def record_login(self, usr):
        status_code = 0
        try:
            user_profile = user.objects.get(fb_id=usr["fb_id"])
            user_profile.first_name = usr["first_name"]
            user_profile.last_name = usr["last_name"]
            user_profile.is_female = usr["is_female"]
            user_profile.email = usr["email"]
            user_profile.coordinate_x = usr["coordinate_x"]
            user_profile.coordinate_y = usr["coordinate_y"]
            user_profile.span_coordinate_x = int(usr["coordinate_x"])
            user_profile.span_coordinate_y = int(usr["coordinate_y"])
            user_profile.is_active = True
            user_profile.save()
        except user.DoesNotExist:
            user(
                fb_id=usr["fb_id"],
                first_name=usr["first_name"],
                last_name=usr["last_name"],
                is_female=usr["is_female"],
                email=usr["email"],
                coordinate_x=usr["coordinate_x"],
                coordinate_y=usr["coordinate_y"],
                span_coordinate_x=int(usr["coordinate_x"]),
                span_coordinate_y=int(usr["coordinate_y"]),
                is_active=True,
            ).save()
            user_obj = user.objects.get(fb_id=usr["fb_id"])
            user_id = user_obj.id
            if 0 < user_id <= 100:
                user_obj.flower_limit = 500
                user_obj.special_limit = 200
                user_obj.save()
                status_code = 100
            if 100 < user_id <= 500:
                user_obj.flower_limit = 200
                user_obj.special_limit = 100
                user_obj.save()
                status_code = 500
            if 500 < user_id <= 1000:
                user_obj.flower_limit = 50
                user_obj.special_limit = 30
                user_obj.save()
                status_code = 1000
        return status_code

    def record_logout(self, user_fb_id):
        user_profile = user.objects.get(fb_id=user_fb_id)
        user_profile.is_active = False
        user_profile.save()
        return 0

    def record_rating(self, from_fb_id, to_fb_id, score, is_flower, is_special):
        try:
            row = user_rating.objects.get(from_fb_id=from_fb_id, to_fb_id=to_fb_id)
            return False
        except user_rating.DoesNotExist:
            user_rating(
                from_fb_id=from_fb_id,
                to_fb_id=to_fb_id,
                score=score,
                is_flower=is_flower,
                is_special=is_special,
                is_rated=False,
            ).save()
            return True

    def record_flower(self, to_fb_id, is_flower, is_special):
        user_info.objects.filter(user_fb_id=to_fb_id).update(
            new_user=user.objects.get(fb_id=to_fb_id),
            rate_times=F("rate_times")+1,
        )
        user_info_obj = user_info.objects.filter(user_fb_id=to_fb_id)
        if is_flower:
            user_info_obj.update(total_flowers=F("total_flowers")+1)
        if is_special:
            user_info_obj.update(total_specials=F("total_specials")+1)
        return 0

    def record_exception(self, user_fb_id, user_flower, current_flower, used_special, current_special):
        user_exception(
            user_fb_id=user_fb_id,
            used_flower=user_flower,
            current_flower=current_flower,
            used_special=used_special,
            current_special=current_special,
        ).save()
        return 0

    def decrease_flower(self, user_fb_id, special_num, flower_num):
        user_obj = user.objects.get(fb_id=user_fb_id)
        user_obj.flower_limit = flower_num
        user_obj.special_limit = special_num
        user_obj.save()
        return True

