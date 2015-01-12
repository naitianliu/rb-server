from django.db import models
import datetime


class user(models.Model):
    last_login = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_female = models.BooleanField()
    email = models.CharField(max_length=75)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField(auto_now_add=True)
    fb_id = models.CharField(max_length=20)
    flower_limit = models.IntegerField(default=3)
    flower_update_time = models.DateTimeField(default=datetime.datetime.now())
    special_limit = models.IntegerField(default=0)
    coordinate_x = models.FloatField()
    coordinate_y = models.FloatField()
    span_coordinate_x = models.IntegerField(max_length=3)
    span_coordinate_y = models.IntegerField(max_length=3)


class user_rating(models.Model):
    from_fb_id = models.CharField(max_length=20)
    to_fb_id = models.CharField(max_length=20)
    score = models.IntegerField()
    is_flower = models.BooleanField()
    is_special = models.BooleanField()
    is_rated = models.BooleanField()
    datetime = models.DateTimeField(auto_now=True)


class user_info(models.Model):
    new_user = models.OneToOneField(user)
    user_fb_id = models.CharField(max_length=20)
    average_score = models.FloatField()
    total_flowers = models.IntegerField(default=0)
    total_specials = models.IntegerField(default=0)
    rate_times = models.IntegerField()
    score_rank = models.IntegerField()
    flower_rank = models.IntegerField()
    special_rank = models.IntegerField()
    score_percentage = models.CharField(max_length=20)
    flower_percentage = models.CharField(max_length=20)
    special_percentage = models.CharField(max_length=20)
    datetime = models.DateTimeField(auto_now=True)


class user_session(models.Model):
    fb_id = models.CharField(max_length=20)
    session_id = models.CharField(max_length=400)
    issued_time = models.DateTimeField()
    expire_time = models.DateTimeField()
    datetime = models.DateTimeField(auto_now=True)


class user_transaction(models.Model):
    user_fb_id = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50)
    purchase_date = models.DateTimeField()
    datetime = models.DateTimeField(auto_now=True)


class user_exception(models.Model):
    user_fb_id = models.CharField(max_length=20)
    used_flower = models.IntegerField(max_length=2)
    current_flower = models.IntegerField(max_length=2)
    used_special = models.IntegerField(max_length=1)
    current_special = models.IntegerField(max_length=1)
    datetime = models.DateTimeField(auto_now=True)


# Create your models here.
