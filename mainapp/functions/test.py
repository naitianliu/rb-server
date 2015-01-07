__author__ = 'gaoxindai'

import math
import time
import datetime
import random
import pytz
from django.utils import timezone


def distance_1(lat_1, lat_2, lng_1, lng_2):
    x = time.time()
    pi = math.pi
    R = 4025.328    # radius of earth /miles
    dlat = abs((lat_1 - lat_2) * pi / 180)
    dlng = abs(((lng_1 - lng_2) * pi / 180))
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat_1 * pi/180) * math.cos(lat_2*pi/180) * math.sin(dlng/2) * math.sin(dlng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    y = time.time()
#    print (y-x)
    return d

def test(lat_1, lat_2, lng_1, lng_2):
    conv_fac = 66
    a = time.time()
    z = conv_fac * math.sqrt(pow((lat_1 - lat_2), 2) + pow((lng_1 - lng_2), 2))
    b = time.time()
    print z
    print (b-a)

def test_2():
    a = time.time()
    x = 42.3245
    y = 56.23123
    z = (x + y) / 9
    b = time.time()
#    print z
#    print (b-a)

def test_3(span, coordinate_x, coordinate_y):
    conv_fac = 66
    coordinate_range = math.sqrt(float(span) / conv_fac)
    x_limit_up = coordinate_x + coordinate_range
    x_limit_down = coordinate_x - coordinate_range
    print x_limit_up, x_limit_down
    y_limit_up = coordinate_y + coordinate_range
    y_limit_down = coordinate_y - coordinate_range
    x = random.uniform(x_limit_up, x_limit_down)
    y = random.uniform(y_limit_up, y_limit_down)
    test(coordinate_x, x, coordinate_y, y)

"""
1.4: 100mi
0,03: 2mi
0.04: 2.8
0.05: 3.5
0.011
"""


if __name__ == "__main__":
#    my_tz = pytz.timezone('US/Pacific')
#    tz = pytz.timezone('Asia/Shanghai')
#    utc = pytz.utc
#    x = datetime.datetime.now()
#    print x
#    print utc
#    n = datetime.datetime.now(tz)
#    print n
#    m = n.astimezone(my_tz).date()
#    print m
    print distance_1(42.0000000, 43.1000000, 38.0000000, 39.1000000)
#    print distance_1(37.4154254, 38.4154254, 38.4154254, 39.4154254)
#    print distance_1(37.4154254, 30.561934, -121.9625374, 114.3403674)
#    test(37.4154254, 38.4154254, 38.4154254, 39.4154254)
#    test(37.4154254, 37.3770091, -121.9625374, -121.9227009)
#    test_2()
#    test_3(50, 37.4154254, -121.9625374)