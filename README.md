rb-server
=========
POST  /user/login/                    user register/login
POST  /user/logout/                   user logout
POST  /user/profile/                  show user profile
POST  /user/records/                  recordes user ratings after logout
POST  /display/neaby/beauties/        display neaby beauties
POST  /display/all/beauties/          display all beauties
POST  /display/neaby/rank/            display neaby rank
POST  /display/all/rank/              display all rank
POST  /user/flower/limit/update/      update every day flower limit
POST  /user/score/calculate/          calculate user average score
POST  /user/buy/flowers/              buy flowers
GET  /global/update/                  update global data

# gender: 0--female, 1--male, 2--both.
# status_code: 0--success, 1--failure

1. /user/login/

request:
    {
        "usr":{
            "session_id": ""
            "fb_id": "",
            "first_name": "",
            "last_name": "",
            "is_female": 1,
            "gender": 2
            "email": "",
            "coordinate":{
                "x": 42.5678,
                "y": 42.1234
            },
        }
    }

response:
{
    "status_code": "0",
    "profile": {
        "special": "0",
        "user_rank_num": "1",
        "flower": "0",
        "special_limit": "200",
        "flower_limit": "500",
        "rater_num": "0",
        "score": "0.0",
        "rank": {
            "flower": {
                "flower_percentage": "0%",
                "flower_rank": "0"
            },
            "score": {
                "score_percentage": "0%",
                "score_rank": "0"
            },
            "special": {
                "special_rank": "0",
                "special_percentage": "0%"
            }
        },
        "coordinate": {
            "y": "40.2736472",
            "x": "40.2736472"
        },
    },
    "display": {
        "beauty_list": []
    }
}

2.  /user/logout

request:
    {
        "fb_id": "",
        "session_id": ""
    }

response:
    {
        "status": "0"
    }
    
3.  /user/profile/

request:
    {
        "fb_id": "",
        "session_id": "",
    }

response:
{
    "status_code": "0",
    "first_name": "Gaoxin",
    "flower": "0",
    "special": "0",
    "rater_num": "0",
    "score": "0.0",
    "rank": {
        "flower": {
            "flower_percentage": "0%",
            "flower_rank": "0"
        },
        "score": {
            "score_percentage": "0%",
            "score_rank": "0"
        },
        "special": {
            "special_rank": "0",
            "special_percentage": "0%"
        }
    },
    "coordinate": {
        "y": "40.2736472",
        "x": "41.1827384"
    },
}  
4.  /user/records/

request:
    {
        "fb_id": "",
        "session_id": "",
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
    
  response:
    {
        "status_code": "0"
    }

5.  /display/nearby/beauties/

request:
    # gender: 0--femal, 1--male, 2--both.
    {
        "fb_id": "",
        "session_id": ""
        "gender": 2,
    }

response:
    {
        "beauty_list": [
            # beauty fb_id, length = 50
            {
                "beauty_fb_id": "529789400456737",
                "first_name": "",
                "score": 9,
                "rater_number":{
                    "score": 8,
                    "flower": 3,
                    "special": 1,
                },
                "flower": 5,
                "special": 1,
                "coordinate":{
                    "x": 42.5678,
                    "y": 42.1234
                },
            }
        ]
    }

6.  /display/all/beauties

request:
    # gender: 0--femal, 1--male, 2--both.
    {
        "fb_id": "",
        "session_id": ""
        "gender": 2,
    }
    
response:
    {
        "beauty_list": [
            # beauty fb_id, length = 50
            {
                "beauty_fb_id": "529789400456737",
                "first_name": "",
                "score": 9,
                "rater_number":{
                    "score": 8,
                    "flower": 3,
                    "special": 1,
                },
                "flower": 5,
                "special": 1,
                "coordinate":{
                    "x": 42.5678,
                    "y": 42.1234
                },
            }
        ]
    }
    
7.   /display/neaby/rank/ 

request:

{
    "fb_id": ""
    "session_id": ""
}

response:
{
    "boys": {
                "score_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank" : 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                }
            }
        ],
        "flower_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank" : 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                },
            }
        ],
        "special_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank": 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                },
            }
        ]    
    }
    "girls":
            "score_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank" : 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                }
            }
        ],
        "flower_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank" : 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                },
            }
        ],
        "special_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank": 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                },
            }
        ]
}

8. /display/all/rank/

request:

{
    "fb_id": fb_id,
    "session_id": "",
}


response:

{
    "boys": {
                "score_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank" : 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                }
            }
        ],
        "flower_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank" : 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                },
            }
        ],
        "special_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank": 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                },
            }
        ]    
    }
    "girls":
            "score_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank" : 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                }
            }
        ],
        "flower_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank" : 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                },
            }
        ],
        "special_rank_list": [
            {
                "fb_id": 529789400456737,
                "first_name": "",
                "rank": 1,
                "rater_number":{
                    "score": 8,
                    "flower": 6,
                    "special": 1,
                },
            }
        ]
}
9. /user/flower/limit/update/

request:

{
    "fb_id": ""
    "datetime": "datetime"
    "session_id":
}

response:
{
    "result": "0",
    "status_code": "0",
}

10. /user/score/calculate/
request:

    {
        "fb_id": ""
        "session_id": ""
    }
response:

{
    "status_code": "0",
    "score": "5.0",
}

11. /global/update/

request:
GET

response:
{
    "status_code":"0"
}
12. /user/buy/flowers/
request:

    {
        "fb_id": ""
        "flower_num": 10
        "special_num": 20
        "session_id": ""
        "receipt_data": ""
    }
    
response:

{
    "status_code": "0"
}
