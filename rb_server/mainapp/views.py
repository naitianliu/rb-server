from django.shortcuts import render, render_to_response, HttpResponse
from django.template import RequestContext, Context, Template
from mainapp.models import *
from django.views.decorators.csrf import csrf_exempt
from mainapp.functions import record_data
from mainapp.functions import db_operation
from mainapp.functions import calculate_data
from mainapp.static import  globals
import datetime
import json
import time
import random
import string
import urllib2
# Create your views here.


@csrf_exempt
def test(request):
    """
    # insert users
    for i in xrange(1, 2000):
        coordinate_x = random.uniform(40, 45)
        coordinate_y = random.uniform(40, 45)
        fb_id = str(i)
        is_female = random.randrange(0, 2),
        email = "daigx1990@gmail.com",
        first_name = "".join(random.sample(string.letters, 5)),
        last_name = "".join(random.sample(string.letters, 5)),
        gender = random.randrange(0, 3)
        url = "http://127.0.0.1:8000/user/login/"
        data = dict(
            usr=dict(
                fb_id=fb_id,
                first_name=first_name,
                last_name=last_name,
                is_female=is_female,
                gender=gender,
                email=email,
                coordinate_x=coordinate_x,
                coordinate_y=coordinate_y
            )
        )
        data = json.dumps(data)
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
    # insert ratings
    for j in xrange(1, 2000):
        fb_id = str(j)
        records_list = []
        for i in range(1, 50):
            beauty_fb_id = str(random.randrange(1, 2000))
            score = random.randrange(1, 11)
            flower = random.randrange(0, 2)
            special = random.randrange(0, 2)
            records_list.append(dict(
                beauty_fb_id=beauty_fb_id,
                score=score,
                flower=flower,
                special=special,
            ))
        data = dict(
            fb_id=fb_id,
            records_list=records_list
        )
        url = "http://127.0.01:8000/user/records/"
        heasers = {"Content-Type": "application/json", "Accept": "application/json"}
        data = json.dumps(data)
        req = urllib2.Request(url, data, heasers)
        response = urllib2.urlopen(req)
    """
    # calculate score
    for i in range(1, 2000):
        url = "http://127.0.0.1:8000/user/score/calculate/"
        data = dict(
            fb_id=str(i)
        )
        data = json.dumps(data)
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
    return render_to_response("test.html", RequestContext(request))

@csrf_exempt
def login(request):
    """
    # gender: 0--female, 1--male, 2--both.
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
    try:
        user_info_obj = user_info.objects.get(user_fb_id=fb_id)
    except user_info.DoesNotExist:
        user_info(
            new_user=user_obj,
            user_fb_id=fb_id,
            average_score=0.000,
            total_flowers=0,
            total_specials=0,
            rate_times=0,
            score_rank=0,
            flower_rank=0,
            special_rank=0,
            score_percentage="0%",
            flower_percentage="0%",
            special_percentage="0%",
        ).save()
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
            special_limit=user_obj.special_limit,
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
    record_data.RecordData().record_logout(fb_id)
    res_data = {
        "status": 1
    }
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def show_profile(request):
    """
    # gender: 0--female, 1--male, 2--both.
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
            x=user_obj.coordinate_x,
            y=user_obj.coordinate_y
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
    # gender: 0--female, 1--male, 2--both.
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
                "special": 1,
            },
            {
                "beauty_fb_id": "",
                "score": 8,
                "flower": 1,
                "special": 1,
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
        flower_num = current_flower - used_flower
        special_num = current_special - used_special
        record_data.RecordData().decrease_flower(fb_id, special_num, flower_num)
        for item in records_list:
            beauty_fb_id = item["beauty_fb_id"]
            score = item["score"]
            is_flower = item["flower"]
            is_special = item["special"]
            if record_data.RecordData().record_rating(fb_id, beauty_fb_id, score, is_flower, is_special):
                record_data.RecordData().record_flower(beauty_fb_id, is_flower, is_special)
    res_data = {
        "success": 1
    }
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
    female_ranked_objects = ranked_obj["female_ranked_objects"]
    male_ranked_objects = ranked_obj["male_ranked_objects"]
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
    female_ranked_objects = globals.female_ranked_object
    male_ranked_objects = globals.male_ranked_object
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
        score=new_average_score,
    )
    calculate_data.CalculateData().cal_user_rank(fb_id)
    return HttpResponse(json.dumps(res_data), content_type="application/json")


def update_global(request):
    db_operation.DbOperation().update_global_var()
    res_data = dict(
        status="1",
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")


def buy_flowers(request):
    """
    POST
    request:
    {
        "fb_id": ""
        "flower_num": 10
        "special_num": 20
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    flower_num = data["flower_num"]
    special_num = data["special_num"]
    db_operation.DbOperation().buy_flowers_op(fb_id, special_num, flower_num)
    res_data = dict(
        status="1",
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")