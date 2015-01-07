from django.shortcuts import render, render_to_response, HttpResponse
from django.template import RequestContext, Context, Template
from mainapp.models import *
from django.views.decorators.csrf import csrf_exempt
from mainapp.functions import record_data
from mainapp.functions import db_operation
from mainapp.functions import calculate_data
import datetime
import json
import time
import random
import string
# Create your views here.


@csrf_exempt

def test(request):
# Total 10000 users
    for i in xrange(1, 100):
        coordinate_x = random.uniform(40, 45)
        coordinate_y = random.uniform(40, 45)
        user(
            fb_id=str(i),
            is_female=random.randrange(0, 2),
            flower_limit=random.randrange(0, 4),
            email="daigx1990@gmail.com",
            coordinate_x=coordinate_x,
            coordinate_y=coordinate_y,
            span_coordinate_x=int(coordinate_x),
            span_coordinate_y=int(coordinate_y),
            first_name="".join(random.sample(string.letters, 5)),
            last_name="".join(random.sample(string.letters, 5)),
            is_active=random.randrange(0, 2),
        ).save()
    print type(user.objects.get(fb_id='10').id)
#   average 100 score times per person
#   user_id= 100:   111 score
#   user_id= 1000:  1094
#   user_id= 10000: 11107
    return render_to_response("test.html", RequestContext(request))

@csrf_exempt
def login(request):
    """
    POST
    request:
    {
        "usr":{
            "fb_id": "",
            "first_name": "",
            "last_name": "",
            "is_female": 1,
            "gender": 2,
            "email": "",
            "coordinate_x": 42.5678,
            "coordinate_y": 42.1234,
        }
    }
    """
    data = json.loads(request.body)
    usr = data["usr"]
    fb_id = usr["fb_id"]
    gender = usr["gender"]
    record_data.RecordData().record_login(usr)
    user_obj = user.objects.get(fb_id=fb_id)
    user_info_obj = user_info.objects.get(user_fb_id=fb_id)
    beauty_fb_id_list = db_operation.DbOperation().cal_display_all_beauties_op(gender)
    try:
        row = user_rating.objects.get(from_fb_id=fb_id)
        beauty_list = calculate_data.CalculateData().cal_display_beauties(fb_id, beauty_fb_id_list)
    except user_rating.DoesNotExist:
        beauty_list = calculate_data.CalculateData().cal_first_display_beauties(beauty_fb_id_list)
    user_id = user_obj.id
    res_data = dict(
        profile=dict(
            user_num=user_id,
            flower=user_info_obj.total_flowers,
            score=user_info_obj.average_score,
            special=user_info_obj.total_specials,
            flower_limit=user_obj.flower_limit,
            coordinate=dict(
                x=user_obj.coordinate_y,
                y=user_obj.coordinate_y,
            ),
            rater_num=user_info_obj.rate_times,
            rank=dict(
                score=dict(
                    score_rank=user_info_obj.score_rank,
                    score_percentage=user_info_obj.score_percentage,
                ),
                flower=dict(
                    flower_rank=user_info_obj.flower_rank,
                    flower_percentage=user_info_obj.flower_percentage,
                ),
                special=dict(
                    special_rank=user_info_obj.special_rank,
                    special_percentage=user_info_obj.special_percentage,
                ),
            )
        ),
        display=dict(
            beauty_list=beauty_list
        )
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def logout(request):
    """
    POST
    request:
    {
        "fb_id": ""
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    print fb_id
    record_data.RecordData().record_logout(fb_id)
    res_data = {
        "status": 1
    }
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def show_profile(request):
    """
    POST
    request:
    {
        "fb_id" : ""
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    user_info_obj = user_info.objects.get(user_fb_id=fb_id)
    user_obj = user.objects.get(fb_id=fb_id)
    res_data = dict(
        first_name=user_obj.first_name,
        flower=user_info_obj.total_flowers,
        score=user_info_obj.average_score,
        special=user_info_obj.total_specials,
        rater_num=user_info_obj.rate_times,
        coordinate=dict(
            x=user.coordinate_x,
            y=user.coordinate_y
        ),
        rank=dict(
            score=dict(
                score_rank=user_info_obj.score_rank,
                score_percentage=user_info_obj.score_percentage,
            ),
            flower=dict(
                flower_rank=user_info_obj.flower_rank,
                flower_percentage=user_info_obj.flower_percentage,
            ),
            special=dict(
                special_rank=user_info_obj.special_rank,
                special_percentage=user_info_obj.special_percentage,
            ),
        )
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def display_nearby_beauties(request):
    """
    POST
    request:
    {
        "fb_id": fb_id,
        "gender": 2
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    gender = data["gender"]
    beauty_fb_id_list = db_operation.DbOperation().cal_display_nearby_beauties_op(gender, fb_id)
    beauty_list = calculate_data.CalculateData().cal_display_beauties(fb_id, beauty_fb_id_list)
    res_data = dict(
        beauty_list=beauty_list
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")


@csrf_exempt
def display_all_beauties(request):
    """
    POST
    request:
    {
        "fb_id": fb_id,
        "gender": 2
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    gender = data["gender"]
    beauty_fb_id_list = db_operation.DbOperation().cal_display_all_beauties_op(gender)
    beauty_list = calculate_data.CalculateData().cal_display_beauties(fb_id, beauty_fb_id_list)
    res_data = dict(
        beauty_list=beauty_list
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def rating_records(request):
    """
    POST
    request:
    {
        "fb_id": "",
        "records_list":[
            {
                "beauty_fb_id": "",
                "score": 9,
                "flower": 1,
                "special": True,
            },
            {
                "beauty_fb_id": "",
                "score": 8,
                "flower": 3,
                "special": True,
            },
        ]
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    records_list = data["records_list"]
    used_flower = 0
    used_special = 0
    for item in records_list:
        used_flower += item["flower"]
        used_special += item["special"]
    current_user = user.objects.get(fb_id=fb_id)
    current_flower = current_user.flower_limit
    current_special = current_user.special_limit
    if current_special < used_special or current_flower < used_flower:
        record_data.RecordData().record_exception(fb_id, used_flower, current_flower, used_special, current_special)
    else:
        for item in records_list:
            beauty_fb_id = item["beauty_fb_id"]
            score = item["score"]
            is_flower = item["flower"]
            is_special = item["special"]
            record_data.RecordData().record_rating(fb_id, beauty_fb_id, score, is_flower, is_special)
            record_data.RecordData().record_flower(fb_id, beauty_fb_id, score, is_flower, is_special)

    res_data = {
        "success": 1
    }
    time.sleep(2)
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def nearby_rank_list(request):
    """
    POST
    request:
    {
        "fb_id": ""
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    ranked_obj = db_operation.DbOperation().cal_nearby_beauty_rank_op(fb_id)
    female_ranked_objects = ranked_obj["female_ranked_obejects"]
    male_ranked_objects = ranked_obj["male_ranked_obejects"]
    female_rank = calculate_data.CalculateData().cal_beauty_rank(female_ranked_objects)
    male_rank = calculate_data.CalculateData().cal_beauty_rank(male_ranked_objects)
    res_data = dict(
        boys=male_rank,
        girls=female_rank,
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")


@csrf_exempt
def all_rank_list(request):
    """
    POST
    request:
    {
        "fb_id": ""
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    ranked_obj = db_operation.DbOperation().all_beauty_rank_op()
    female_ranked_objects = ranked_obj["female_ranked_obejects"]
    male_ranked_objects = ranked_obj["male_ranked_obejects"]
    female_rank = calculate_data.CalculateData().cal_beauty_rank(female_ranked_objects)
    male_rank = calculate_data.CalculateData().cal_beauty_rank(male_ranked_objects)
    res_data = dict(
        boys=male_rank,
        girls=female_rank,
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def flower_limit_update(request):
    """
    POST
    request:
    {
        "fb_id": ""
        "datetime": "datetime"
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    user_datetime = data["datetime"]
    result = db_operation.DbOperation().update_flower_limit(fb_id, user_datetime)
    res_data = dict(
        result=result
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def cal_user_score(request):
    """
    POST
    request:
    {
        "fb_id": ""
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    user_info_obj = user_info.objects.get(user_fb_id=fb_id)
    rate_times = user_info_obj.rate_times
    average_score = user_info_obj.average_score
    new_average_score = calculate_data.CalculateData().cal_user_score(fb_id, rate_times, average_score)
    user_info_obj.average_score = new_average_score
    user_info_obj.save()
    res_data = dict(
        status="1"
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")


def update_global(request):
    db_operation.DbOperation().update_global_var()
    res_data = dict(
        status="1",
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")