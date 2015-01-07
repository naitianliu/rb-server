__author__ = 'gaoxindai'

from mainapp.models import user_info
from mainapp.models import user_rating
from mainapp.models import user
from mainapp.static import globals
from mainapp.static.constant import span_fac
from django.db.models import Q
from mainapp.static.constant import server_tz
from mainapp.static import globals
import pytz
import datetime


class DbOperation(object):

    def __init__(self):
        pass

    def cal_display_all_beauties_op(self, gender):
        # female
        if gender == 1:
            beauty_fb_id_list = globals.female_beauty_fb_id_list
        # male
        if gender == 0:
            beauty_fb_id_list = globals.male_beauty_fb_id_list
        # both
        else:
            beauty_fb_id_list = globals.all_beauty_fb_id_list
        return beauty_fb_id_list

    def all_beauty_rank_op(self):
        female_ranked_obejects = globals.female_beauty_fb_id_list
        male_ranked_obejects = globals.male_beauty_fb_id_list
        ranked_object = dict(
            female_ranked_obejects=female_ranked_obejects,
            male_ranked_obejects=male_ranked_obejects
        )
        return ranked_object

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
            all_records = user.objects.filter(Q(is_female=True), Q(span_coordinate_x=x_limit_up) | Q(span_coordinate_x=x_limit_down), Q(span_coordinate_y=y_limit_up) | Q(span_coordinate_y=y_limit_down))
        # male
        if gender == 0:
            all_records = user.objects.filter(Q(is_female=False), Q(span_coordinate_x=x_limit_up) | Q(span_coordinate_x=x_limit_down), Q(span_coordinate_y=y_limit_up) | Q(span_coordinate_y=y_limit_down))
        # both
        else:
            all_records = user.objects.filter(Q(span_coordinate_x=x_limit_up) | Q(span_coordinate_x=x_limit_down), Q(span_coordinate_y=y_limit_up) | Q(span_coordinate_y=y_limit_down))
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
        female_ranked_obejects = user_info.obejcts.filter(Q(user_is_female=True), Q(user_span_coordinate_x=x_limit_up) | Q(user_span_coordinate_x=x_limit_down), Q(user_span_coordinate_y=y_limit_up) | Q(user_span_coordinate_y=y_limit_down)).order_by("-average_score")[0:50]
        male_ranked_obejects = user_info.obejcts.filter(Q(user_is_female=False), Q(user_span_coordinate_x=x_limit_up) | Q(user_span_coordinate_x=x_limit_down), Q(user_span_coordinate_y=y_limit_up) | Q(user_span_coordinate_y=y_limit_down)).order_by("-average_score")[0:50]
        ranked_object = dict(
            female_ranked_obejects=female_ranked_obejects,
            male_ranked_obejects=male_ranked_obejects
        )
        return ranked_object

    def update_global_var(self):
        # female
        globals.female_beauty_fb_id_list = list(user.objects.filter(is_female=True).values_list("fb_id", flat=True))
        globals.female_ranked_object = user_info.obejcts.filter(user_is_female=True).order_by("-average_score")[0:50]
        # male
        globals.male_beauty_fb_id_list = list(user.objects.filter(is_female=False).values_list("fb_id", flat=True))
        globals.male_ranked_object = user_info.obejcts.filter(user_is_female=False).order_by("-average_score")[0:50]
        # both
        globals.all_beauty_fb_id_list = list(user.objects.all().values_list("fb_id", flat=True))
        return True

    def update_flower_limit(self, user_fb_id, user_datetime):
        user_obj = user.objects.get(fb_id=user_fb_id)
        flower_limit = user_obj.flower_limit
        my_tz = pytz.timezone(server_tz)
        user_date = user_datetime.astimezone(my_tz).date()
        user_db_date = user_obj.flower_update_time.date()
        if flower_limit < 3 and user_date == user_db_date:
            user_obj.flower_limit = 3
            user_obj.flower_update_time = datetime.datetime.now()
            user_obj.save()
            return True
        else:
            return False




