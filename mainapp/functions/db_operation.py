__author__ = 'gaoxindai'

from mainapp.models import user_info
from mainapp.models import user_rating
from mainapp.models import user
from mainapp.static import globals
from mainapp.static.constant import span_fac
from django.db.models import Q
from mainapp.static.constant import server_tz
from mainapp.static import globals
import datetime


class DbOperation(object):

    def __init__(self):
        pass

    def cal_display_all_beauties_op(self, gender, fb_id):
        # female
        if gender == 1:
            beauty_fb_id_list = globals.female_beauty_fb_id_list
        # male
        if gender == 0:
            beauty_fb_id_list = globals.male_beauty_fb_id_list
        # both
        else:
            beauty_fb_id_list = globals.all_beauty_fb_id_list
        try:
            beauty_fb_id_list.remove(fb_id)
        except:
            pass
        return beauty_fb_id_list


    def cal_display_nearby_beauties_op(self, gender, user_fb_id):
        user_obj = user.objects.get(fb_id=user_fb_id)
        span_coordinate_x = user_obj.span_coordinate_x
        span_coordinate_y = user_obj.span_coordinate_y
        x_limit_up = span_coordinate_x + span_fac
        y_limit_up = span_coordinate_y + span_fac
        x_limit_down = span_coordinate_x - span_fac
        y_limit_down = span_coordinate_y - span_fac
        # female
        if gender == 1:
            all_records = user.objects.filter(Q(is_female=True), Q(span_coordinate_x=x_limit_up) | Q(span_coordinate_x=x_limit_down), Q(span_coordinate_y=y_limit_up) | Q(span_coordinate_y=y_limit_down)).exclude(fb_id=user_fb_id)
        # male
        if gender == 0:
            all_records = user.objects.filter(Q(is_female=False), Q(span_coordinate_x=x_limit_up) | Q(span_coordinate_x=x_limit_down), Q(span_coordinate_y=y_limit_up) | Q(span_coordinate_y=y_limit_down)).exclude(fb_id=user_fb_id)
        # both
        else:
            all_records = user.objects.filter(Q(span_coordinate_x=x_limit_up) | Q(span_coordinate_x=x_limit_down), Q(span_coordinate_y=y_limit_up) | Q(span_coordinate_y=y_limit_down)).exclude(fb_id=user_fb_id)
        beauty_fb_id_list = list(all_records.values_list("fb_id", flat=True))
        return beauty_fb_id_list

    def cal_nearby_beauty_rank_op(self, user_fb_id):
        user_obj = user.objects.get(fb_id=user_fb_id)
        span_coordinate_x = user_obj.span_coordinate_x
        span_coordinate_y = user_obj.span_coordinate_y
        x_limit_up = span_coordinate_x + span_fac
        y_limit_up = span_coordinate_y + span_fac
        x_limit_down = span_coordinate_x - span_fac
        y_limit_down = span_coordinate_y - span_fac
        female_ranked_objects = user_info.objects.filter(Q(new_user__is_female=True), Q(new_user__span_coordinate_x=x_limit_up) | Q(new_user__span_coordinate_x=x_limit_down), Q(new_user__span_coordinate_y=y_limit_up) | Q(new_user__span_coordinate_y=y_limit_down)).order_by("-average_score")
        if len(female_ranked_objects) > 50:
            female_ranked_objects = female_ranked_objects[0:50]
        male_ranked_objects = user_info.objects.filter(Q(new_user__is_female=True), Q(new_user__span_coordinate_x=x_limit_up) | Q(new_user__span_coordinate_x=x_limit_down), Q(new_user__span_coordinate_y=y_limit_up) | Q(new_user__span_coordinate_y=y_limit_down)).order_by("-average_score")
        if len(male_ranked_objects) > 50:
            male_ranked_objects = male_ranked_objects[0:50]
        ranked_object = dict(
            female_ranked_objects=female_ranked_objects,
            male_ranked_objects=male_ranked_objects,
        )
        return ranked_object

    def update_global_var(self):
        # female
        try:
            globals.female_beauty_fb_id_list = list(user.objects.filter(is_female=True).values_list("fb_id", flat=True))
        except:
            globals.female_beauty_fb_id_list = []
        try:
            globals.female_ranked_object = user_info.objects.filter(new_user__is_female=True).order_by("-average_score")
            if len(globals.female_ranked_object) > 50:
                globals.female_ranked_object = globals.female_ranked_object[0:50]
            print 1
        except:
            globals.female_ranked_object = []
            print 2
        try:
            # male
            globals.male_beauty_fb_id_list = list(user.objects.filter(is_female=False).values_list("fb_id", flat=True))
        except:
            globals.male_beauty_fb_id_list = []
        try:
            globals.male_ranked_object = user_info.objects.filter(new_user__is_female=True).order_by("-average_score")
            if len(globals.male_ranked_object) > 50:
                globals.male_ranked_object = globals.male_ranked_object[0:50]
        except:
            globals.male_ranked_object = []
        try:
            # both
            globals.all_beauty_fb_id_list = list(user.objects.all().values_list("fb_id", flat=True))
        except:
            globals.all_beauty_fb_id_list = []
        return 0

    def update_flower_limit(self, user_fb_id, epoch):
        user_obj = user.objects.get(fb_id=user_fb_id)
        flower_limit = user_obj.flower_limit
        user_date = datetime.datetime.fromtimestamp(epoch)
        user_db_date = user_obj.flower_update_time.date()
        if flower_limit < 3 and user_date.date() > user_db_date:
            user_obj.flower_limit = 3
            user_obj.flower_update_time = user_date
            user_obj.save()
            return 0
        else:
            return 4

    def buy_flowers_op(self, user_fb_id, special_num, flower_num):
        user_obj = user.objects.get(fb_id=user_fb_id)
        current_flower = user_obj.flower_limit
        current_special = user_obj.special_limit
        user_obj.flower_limit = current_flower + flower_num
        user_obj.special_limit = current_special + special_num
        user_obj.save()
        return 0




