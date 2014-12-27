rb-server
=========
POST  /user/login/                    user register/login
POST  /user/logout/                   user logout
POST  /user/profile/                  show user profile
POST  /user/records/                  recordes user ratings after logout
POST  /display/beauties/              display pictures of beauties
POST  /display/rank/                  display rank of score/flower/special according to distance
GET  /display/beauty/profile/<fb_id>  display beauty profile on rank list

1. /user/login/

request:
    {
        "usr":{
            "fb_id": "",
            "first_name": "",
            "last_name": "",
            "is_female": True,
            "email": "",
            "coordinate":{
                "x": 42.5678,
                "y": 42.1234
            },
        }
    }

response:
    {
        "status": 1,
        "profile": {
            "flower": 5,
            "score": 8,
            "special": 2,
            "flower_limit": 3,
            "coordinate":{
                "x": 42.5678,
                "y": 42.1234
            },
            "rater_number":{
                "score": 6,
                "flower": 3,
                "special": 1,
            },
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
            }
        },
        "display": {
            "beauty_list": [
                # beauty fb_id, length = 50
                {
                    "beauty_fb_id": "529789400456737",
                    "first_name": "",
                    "score": 9,
                    "flower": 5,
                    "special": 1,
                    "coordinate":{
                        "x": 42.5678,
                        "y": 42.1234
                    },
                    "rater_number":{
                        "score": 5,
                        "flower": 3,
                        "special": 2,
                    },
                }
            ]
        }
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
        "first_name": "",
        "flower": 5,
        "score": 8,
        "special": 2,
        "flower_limit": 3,
        "coordinate":{
            "x": 42.5678,
            "y": 42.1234,
        },
        rater_number:{
            "score": 10,
            "flower": 5,
            "special": 2,
        },
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
    # gender: 0--femal, 1--male, 2--both.
    {
        "fb_id": "",
        "coordinate":{
            "x": 42.5678,
            "y": 42.1234
        },
        "span": 50,
        "gender": 1,
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

6.  /display/rank/

request:
   {
        "coordinate":{
            "x": 42.5678,
            "y": 42.1234
        },
        "span": 50,
    }
    
response:
    {
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
    
7.   /display/beauty/profile/ 

request:

{
    "fb_id": "",
}

response:
    {
        "first_name": "",
        "flower": 5,
        "score": 8,
        "special": 2,
        "flower_limit": 3,
        "coordinate":{
            "x": 42.5678,
            "y": 42.1234,
        },
        rater_number:{
            "score": 10,
            "flower": 5,
            "special": 2,
        },
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
        }
    }
    
