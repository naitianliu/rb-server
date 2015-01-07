__author__ = 'gaoxindai'

from mainapp.models import user_rating
from mainapp.models import user
from mainapp.models import user_info
from random import sample
from mainapp.static.constant import beauty_list_len


class CalculateData(object):

    def __init__(self):
        pass

    def cal_user_score(self, user_fb_id, rate_times, average_score):
        sum_score = rate_times * average_score
        user_rating_obj = user_rating.objects.filter(to_fb_id=user_fb_id, is_rated=False)
        score_list = user_rating_obj.values("score")
        for item in score_list:
            sum_score += item.score
        average_score = round(float(sum_score) / (len(score_list) + rate_times), 3)
        user_rating_obj.update(is_rated=True)
        return average_score

    def cal_first_display_beauties(self, beauty_fb_id_list):
        i = 0
        beauty_list = []
        for item in beauty_fb_id_list:
            beauty_fb_id = item.fb_id
            i += 1
            user_profile = user.objects.get(fb_id=beauty_fb_id)
            user_rating_info = user_info.objects.get(user_fb_id=beauty_fb_id)
            beauty_list.append(dict(
                beauty_fb_id=beauty_fb_id,
                first_name=user_profile.first_name,
                score=user_rating_info.average_score,
                flower_num=user_rating_info.total_flowers,
                special_num=user_rating_info.total_specials,
                rater_num=user_rating_info.rate_times,
                coordinate=dict(
                    x=user_profile.coordinate_x,
                    y=user_profile.coordinate_y,
                )
            ))
            if i == 50:
                break
        return beauty_list

    def cal_display_beauties(self, user_fb_id, beauty_fb_id_list):
        beauty_list = []
        user_to_fb_id_list = list(user_rating.objects.filter(from_fb_id=user_fb_id).values_list("to_fb_id", flat=True))
        display_fb_id_list = list(set(beauty_fb_id_list).difference(set(user_to_fb_id_list)))
        if len(display_fb_id_list) >= beauty_list_len:
            display_fb_id_list = sample(display_fb_id_list, beauty_list_len)
        for beauty_fb_id in display_fb_id_list:
            user_profile = user.objects.get(fb_id=beauty_fb_id)
            user_rating_info = user_info.objects.get(user_fb_id=beauty_fb_id)
            beauty_list.append(dict(
                beauty_fb_id=beauty_fb_id,
                first_name=user_profile.first_name,
                score=user_rating_info.average_score,
                flower_num=user_rating_info.total_flowers,
                special_num=user_rating_info.total_specials,
                rater_num=user_rating_info.rate_times,
                coordinate=dict(
                    x=user_profile.coordinate_x,
                    y=user_profile.coordinate_y,
                )
            ))
        return beauty_list

    def cal_beauty_rank(self, ranked_objects):
        flower_rank_list = []
        score_rank_list = []
        special_rank_list = []
        for record in ranked_objects:
            flower_rank_list.append(dict(
                beauty_fb_id=record.user_fb_id,
                first_name=record.user.firstname,
                score=record.average_score,
                rank=record.flower_rank,
                flower=record.total_flowers,
                special=record.total_specials,
                rater_num=record.rate_times,
                coordinate=dict(
                    x=record.user.coordinate_x,
                    y=record.user.coordinate_y,
                ),
            ))
            score_rank_list.append(dict(
                beauty_fb_id=record.user_fb_id,
                first_name=record.user.firstname,
                score=record.average_score,
                rank=record.score_rank,
                flower=record.total_flowers,
                special=record.total_specials,
                rater_num=record.rate_times,
                coordinate=dict(
                    x=record.user.coordinate_x,
                    y=record.user.coordinate_y,
                ),
            ))
            special_rank_list.append(dict(
                beauty_fb_id=record.user_fb_id,
                first_name=record.user.firstname,
                score=record.average_score,
                rank=record.special_rank,
                flower=record.total_flowers,
                special=record.total_specials,
                rater_num=record.rate_times,
                coordinate=dict(
                    x=record.user.coordinate_x,
                    y=record.user.coordinate_y,
                ),
            ))
        data = dict(
            flower_rank=flower_rank_list,
            score_rank=score_rank_list,
            special_rank=special_rank_list,
        )
        return data

    def cal_user_rank(self, user_fb_id):
        all_records = user_info.objects.all()
        user_info_obj = user_info.objects.get(user_fb_id=user_fb_id)
        user_average_score = user_info_obj.average_score
        user_total_flowers = user_info_obj.total_flowers
        user_total_specials = user_info_obj.total_specials
        higher_score_objects = all_records.filter(average_score__gt=user_average_score)
        score_rank = len(higher_score_objects)
        score_percentage = '%.2f%s' % ((float(score_rank)) / len(all_records), "%")
        higher_flower_objects = all_records.filter(total_flowers__gt=user_total_flowers)
        flower_rank = len(higher_flower_objects)
        flower_percentage = '%.2f%s' % ((float(flower_rank)) / len(all_records), "%")
        higher_special_objects = all_records.filter(total_specials__gt=user_total_specials)
        special_rank = len(higher_special_objects)
        special_percentage = '%.2f%s' % ((float(special_rank)) / len(all_records), "%")
        score_rank = dict(
            score_rank=score_rank,
            score_percentage=score_percentage,
        )
        flower_rank = dict(
            flower_rank=flower_rank,
            flower_percentage=flower_percentage,
        )
        special_rank = dict(
            special_rank=special_rank,
            special_percentage=special_percentage,
        )
        rank_info = dict(
            flower_rank=flower_rank,
            score_rank=score_rank,
            special_rank=special_rank
        )
        return rank_info