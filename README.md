rb-server
=========
POST  /user/login/                  user register/login
POST  /user/logout/                 user logout
POST  /user/profile/                show user profile
POST  /user/records/                recordes user ratings after logout
POST  /display/beauties/            display pictures of beauties
POST  /display/rank/                display rank of score/flower/special according to distance


1. /user/login/

request:
    {
        "usr":{
            "fb_id": "",
            "first_name": "",
            "last_name": "",
            "is_female": True,
            "email": "",
            "coordinate_x": 42.5678,
            "coordinate_y": 42.1234,
        }
    }

response:
    {
        "status": 1
    }

2.  /user/logout

request:
    {
        "fb_id": ""
    }

response:
    {
        "status": 1
    }
    
3.  /user/profile/

request:
    {
        "fb_id": ""
    }

response:
    {
        "flower": 5,
        "score": 8,
        "special": 2,
        "flower_limit": 3,
        "rank": {
            "score": {
                "number": 1,
                "percentage": "100%",
            },
            "flower": {
                "number": 1,
                "percentage": "100%",
            },
            "special": {
                "number": 1,
                "percentage": "100%",
            },
        "coordinate": {
            "x": 42.5678,
            "y": 42.1234,
            }
        }
    }

4.  /user/records/

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
                "flower": 3,
                "special": 1,
            },
        ]
    }
    
  response:
    {
        "success": 1
    }

5.  /display/beauties/

request:
    {
        "fb_id": "",
        "coordinate_x": 42.123,
        "coordinate_y": 42.123,
        "span": 50
    }

response:
    {
        "beauty_list": [
            # beauty fb_id, length = 50
            {
                "beauty_fb_id": "529789400456737",
                "score": 9,
                "rater_number": 1,
                "flower": 5,
                "special": 1,
                "coordinate": {
                    "x": 42.56732,
                    "y": 42.56732,
                }
            }
        ]
    }

6.  /display/rank/

request:
   {
        "coordinate_x": 42.123,
        "coordinate_y": 42.123,
        "span": 50,
    }
    
response:
    {
        "score_rank_list": [
            {
                "fb_id": 529789400456737,
                "rank" : 1,
            }
        ],
        "flower_rank_list": [
            {
                "fb_id": 529789400456737,
                "rank" : 1,
            }
        ],
        "special_rank_list": [
            {
                "fb_id": 529789400456737,
                "rank": 1,
            }
        ]
    }
    
