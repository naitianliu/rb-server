from django.shortcuts import render, render_to_response, HttpResponse
from django.template import RequestContext, Context, Template
from mainapp.models import *
from django.views.decorators.csrf import csrf_exempt
from mainapp.functions import record_data
from mainapp.functions import db_operation
from mainapp.functions import calculate_data
from mainapp.static import globals
from mainapp.functions import access
from mainapp.static import constant
from mainapp.functions import verify_receipt
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
    access_token_url = constant.get_access_token_api
    req_access = urllib2.Request(access_token_url)
    res_access = urllib2.urlopen(req_access)
    data_access = res_access.read()
    access_token = data_access[13:]
    input_token = "CAAIw1KrlSyYBAJ2JMLRlE2133LLtejMolxBbstjZAHzZAGBkkQixCoBnRKU73pNz4zChR2jdNBKaynmhItsNqMdfaYdjQJpUV3ZCbm7gSNPReQlGRmcj2pbOyYOLGfHAHP5fESw59TCb09aqWmZBrZBEceI2CElQ5ZC2ZAj9ZCXg62sRPHWsfMIPy864ZC2qdf0kh8bP08Dq4vWmDMiTprfPj9ROTrmsnsLE8SZAZCqtKq1abZBJs8mt13Go"
    validate_token_url = constant.validate_fb_token_api % (input_token, access_token)
    req_validate = urllib2.Request(validate_token_url)
    res_validate = urllib2.urlopen(req_validate)
    data_validate = res_validate.read()
    data_validate = json.loads(data_validate)
    is_valid = data_validate["data"]["is_valid"]
    expire_time = datetime.datetime.fromtimestamp(data_validate["data"]["expires_at"])
    issued_time = datetime.datetime.fromtimestamp(data_validate["data"]["issued_at"])
    print is_valid, expire_time, issued_time
    """
    validate_receipt_api = constant.validate_receipt_api
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    receipt_data = "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"
    data = {"receipt-data": receipt_data}
    data = json.dumps(data)
    req = urllib2.Request(validate_receipt_api, data, headers)
    res = urllib2.urlopen(req)
    receipt_info_json = res.read()
    receipt_info = json.loads(receipt_info_json)
    for item in receipt_info["receipt"]["in_app"]:
        print item["transaction_id"],
        print item['purchase_date_pst']
    print receipt_info["receipt"]["request_date_pst"]
    return render_to_response("test.html", RequestContext(request))

@csrf_exempt
def login(request):
    """
    gender: 0--female, 1--male, 2--both.
    status_code: 0--success, 1--internal failure, 2--invalid session id,3--session id doesnt match action fb id,
    100--top 100 users, 500--top 500 users, 1000, top 1000 users,
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
            "session_id": 1234567
        }
    }
    """
    data = json.loads(request.body)
    usr = data["usr"]
    fb_id = usr["fb_id"]
    gender = usr["gender"]
    session_id = usr["session_id"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
        status_code = record_data.RecordData().record_login(usr)
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
        beauty_fb_id_list = db_operation.DbOperation().cal_display_all_beauties_op(gender, fb_id)
        try:
            row = user_rating.objects.get(from_fb_id=fb_id)
            beauty_list = calculate_data.CalculateData().cal_display_beauties(fb_id, beauty_fb_id_list)
        except user_rating.DoesNotExist:
            beauty_list = calculate_data.CalculateData().cal_first_display_beauties(beauty_fb_id_list)
        user_id = user_obj.id
        res_data = dict(
            status_code=str(status_code),
            profile=dict(
                user_register_num=str(user_id),
                flower=str(user_info_obj.total_flowers),
                score=str(user_info_obj.average_score),
                special=str(user_info_obj.total_specials),
                flower_limit=str(user_obj.flower_limit),
                special_limit=str(user_obj.special_limit),
                coordinate=dict(
                    x=str(user_obj.coordinate_y),
                    y=str(user_obj.coordinate_y),
                ),
                rater_num=str(user_info_obj.rate_times),
                rank=dict(
                    score=dict(
                        score_rank=str(user_info_obj.score_rank),
                        score_percentage=user_info_obj.score_percentage,
                    ),
                    flower=dict(
                        flower_rank=str(user_info_obj.flower_rank),
                        flower_percentage=user_info_obj.flower_percentage,
                    ),
                    special=dict(
                        special_rank=str(user_info_obj.special_rank),
                        special_percentage=user_info_obj.special_percentage,
                    ),
                )
            ),
            display=dict(
                beauty_list=beauty_list,
            )
        )
    else:
        res_data = dict(
            status_code=str(status_code),
            fb_id=fb_id
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def logout(request):
    """
    status_code: 0--success, 1--internal failure, 2--invalid session id,3--session id doesnt match action fb id
    POST
    request:
    {
        "fb_id": ""
        "session_id": ""
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    session_id = data["session_id"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
        status = record_data.RecordData().record_logout(fb_id)
        res_data = dict(
            status_code=str(status),
        )
    else:
        res_data = dict(
            status_code=str(status_code),
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def show_profile(request):
    """
    status_code: 0--success, 1--internal failure, 2--invalid session id,3--session id doesnt match action fb id
    POST
    request:
    {
        "fb_id" : ""
        "session_id": ""
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    session_id = data["session_id"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
        user_info_obj = user_info.objects.get(user_fb_id=fb_id)
        user_obj = user.objects.get(fb_id=fb_id)
        res_data = dict(
            status_code=str(status_code),
            first_name=user_obj.first_name,
            flower=str(user_info_obj.total_flowers),
            score=str(user_info_obj.average_score),
            special=str(user_info_obj.total_specials),
            rater_num=str(user_info_obj.rate_times),
            coordinate=dict(
                x=str(user_obj.coordinate_x),
                y=str(user_obj.coordinate_y),
            ),
            rank=dict(
                score=dict(
                    score_rank=str(user_info_obj.score_rank),
                    score_percentage=user_info_obj.score_percentage,
                ),
                flower=dict(
                    flower_rank=str(user_info_obj.flower_rank),
                    flower_percentage=str(user_info_obj.flower_percentage),
                ),
                special=dict(
                    special_rank=str(user_info_obj.special_rank),
                    special_percentage=user_info_obj.special_percentage,
                ),
            )
        )
    else:
        res_data = dict(
            status_code=str(status_code),
            fb_id=fb_id,
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

"""
@csrf_exempt
def display_nearby_beauties(request):
    # gender: 0--female, 1--male, 2--both.
    POST
    request:
    {
        "fb_id": fb_id,
        "gender": 2
        "session_id": ""
    }
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    gender = data["gender"]
    session_id = data["session_id"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
        beauty_fb_id_list = db_operation.DbOperation().cal_display_nearby_beauties_op(gender, fb_id)
        beauty_list = calculate_data.CalculateData().cal_display_beauties(fb_id, beauty_fb_id_list)
        res_data = dict(
            status_code=str(status_code),
            beauty_list=beauty_list,
        )
    else:
        res_data = dict(
            status_code=str(status_code),
            fb_id=fb_id,
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")
"""


@csrf_exempt
def display_all_beauties(request):
    """
    status_code: 0--success, 1--internal failure, 2--invalid session id,3--session id doesnt match action fb id
    # is_span: 0--all, 1--nearby
    POST
    request:
    {
        "fb_id": fb_id,
        "gender": 2
        "session_id": ""
        "is_span": 1
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    gender = data["gender"]
    session_id = data["session_id"]
    is_span = data["is_span"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
        if not is_span:
            beauty_fb_id_list = db_operation.DbOperation().cal_display_all_beauties_op(gender, fb_id)
            beauty_list = calculate_data.CalculateData().cal_display_beauties(fb_id, beauty_fb_id_list)
        else:
            beauty_fb_id_list = db_operation.DbOperation().cal_display_nearby_beauties_op(gender, fb_id)
            beauty_list = calculate_data.CalculateData().cal_display_beauties(fb_id, beauty_fb_id_list)
        res_data = dict(
            beauty_list=beauty_list,
            status_code=str(status_code),
        )
    else:
        res_data = dict(
            status_code=str(status_code),
            fb_id=fb_id,
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def rating_records(request):
    """
    status_code: 0--success, 1--internal failure, 2--invalid session id,3--session id doesnt match action fb id
    4--overflow flowers or specials
    POST
    request:
    {
        "session_id": ""
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
    session_id = data["session_id"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
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
            status_code = 4
        else:
            flower_num = current_flower - used_flower
            special_num = current_special - used_special
            record_data.RecordData().decrease_flower(fb_id, special_num, flower_num)
            for item in records_list:
                beauty_fb_id = item["beauty_fb_id"]
                score = item["score"]
                is_flower = item["flower"]
                is_special = item["special"]
                record_data.RecordData().record_rating(fb_id, beauty_fb_id, score, is_flower, is_special)
                record_data.RecordData().record_flower(beauty_fb_id, is_flower, is_special)
        res_data = dict(
            status_code=str(status_code),
        )
    else:
        res_data = dict(
            status_code=str(status_code),
            fb_id=fb_id,
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

"""
@csrf_exempt
def nearby_rank_list(request):
    POST
    request:
    {
        "fb_id": ""
        "session_id": ""
    }
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    session_id = data["session_id"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
        ranked_obj = db_operation.DbOperation().cal_nearby_beauty_rank_op(fb_id)
        female_ranked_objects = ranked_obj["female_ranked_objects"]
        male_ranked_objects = ranked_obj["male_ranked_objects"]
        female_rank = calculate_data.CalculateData().cal_beauty_rank(female_ranked_objects)
        male_rank = calculate_data.CalculateData().cal_beauty_rank(male_ranked_objects)
        res_data = dict(
            status_code=str(status_code),
            boys=male_rank,
            girls=female_rank,
        )
    else:
        res_data = dict(
            status_code=str(status_code),
            fb_id=fb_id,
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")
"""

@csrf_exempt
def all_rank_list(request):
    """
    status_code: 0--success, 1--internal failure, 2--invalid session id,3--session id doesnt match action fb id
    # is_span: 0--all, 1--nearby
    POST
    request:
    {
        "fb_id": ""
        "session_id": ""
        "is_span": 1
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    session_id = data["session_id"]
    is_span = data["is_span"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
        if not is_span:
            female_ranked_objects = globals.female_ranked_object
            male_ranked_objects = globals.male_ranked_object
            female_rank = calculate_data.CalculateData().cal_beauty_rank(female_ranked_objects)
            male_rank = calculate_data.CalculateData().cal_beauty_rank(male_ranked_objects)
        else:
            ranked_obj = db_operation.DbOperation().cal_nearby_beauty_rank_op(fb_id)
            female_ranked_objects = ranked_obj["female_ranked_objects"]
            male_ranked_objects = ranked_obj["male_ranked_objects"]
            female_rank = calculate_data.CalculateData().cal_beauty_rank(female_ranked_objects)
            male_rank = calculate_data.CalculateData().cal_beauty_rank(male_ranked_objects)
        res_data = dict(
            status_code=str(status_code),
            boys=male_rank,
            girls=female_rank,
        )
    else:
        res_data = dict(
            status_code=str(status_code),
            fb_id=fb_id,
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def flower_limit_update(request):
    """
    status_code: 0--success, 1--internal failure, 2--invalid session id,3--session id doesnt match action fb id
    4--invalid update
    POST
    request:
    {
        "fb_id": ""
        "epoch": 1234567890
        "session_id":
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    epoch = data["epoch"]
    session_id = data["session_id"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
        status_code = db_operation.DbOperation().update_flower_limit(fb_id, epoch)
        res_data = dict(
            status_code=str(status_code),
        )
    else:
        res_data = dict(
            status_code=str(status_code),
            fb_id=fb_id,
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
        score=str(new_average_score),
        status_code="0",
    )
    calculate_data.CalculateData().cal_user_rank(fb_id)
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def update_global(request):
    status_code = db_operation.DbOperation().update_global_var()
    res_data = dict(
        status_code=str(status_code),
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")

@csrf_exempt
def buy_flowers(request):
    """
    POST
   status_code: 0--success, 1--internal failure, 2--invalid session id,3--session id doesnt match action fb id
   4--exisiting receipt, 5--invalid receipt
    request:
    {
        "fb_id": ""
        "flower_num": 10
        "special_num": 20
        "session_id": ""
        "receipt_data": ""
    }
    """
    data = json.loads(request.body)
    fb_id = data["fb_id"]
    session_id = data["session_id"]
    receipt_data = data["receipt_data"]
    status_code = access.Access().check_access(fb_id, session_id)
    if not status_code:
        status_code = verify_receipt.VerifyReceipt().check_purchase(fb_id, receipt_data, status_code)
        if not status_code:
            flower_num = data["flower_num"]
            special_num = data["special_num"]
            status = db_operation.DbOperation().buy_flowers_op(fb_id, special_num, flower_num)
            res_data = dict(
                status_code=str(status),
            )
        else:
            res_data = dict(
                status_code=str(status_code),
            )
    else:
        res_data = dict(
            status_code=str(status_code),
            fb_id=fb_id,
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")