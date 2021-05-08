from datetime import datetime

from django.db import models


# Create your models here.

# 用户表
class UserEntity(models.Model):
    username = models.CharField(max_length=255)  # 用户昵称
    mobile = models.CharField(max_length=255)  # 用户电话
    password = models.CharField(max_length=255)  # 密码
    email = models.CharField(max_length=255)  # 邮箱
    wallet = models.IntegerField(default=0)  # 余额
    gender = models.CharField(max_length=10)  # 性别
    user_img = models.CharField(max_length=500)  # 用户头像
    status = models.IntegerField(default=0)  # 0属于正常用户
    add_time = models.DateField(auto_now=True)  # 创建时间

    class Meta:
        db_table = 'user'


# 地址表
class Address(models.Model):
    user_id = models.IntegerField()  # 绑定的用户
    username = models.CharField(max_length=255)  # 用户昵称
    gender = models.CharField(max_length=10)  # 用户性别
    mobile = models.CharField(max_length=255)  # 电话
    address = models.CharField(max_length=255)  # 配送地址
    default = models.IntegerField(default=1)  # 1代表默认地址
    status = models.IntegerField(default=0)  # 0代表正常状态
    tag = models.CharField(max_length=255)  # 标签

    class Meta:
        db_table = 'address'


# 店铺收藏表
class ShopCollect(models.Model):
    shop_id = models.IntegerField()  # 商铺ID
    user_id = models.IntegerField()  # 用户ID
    shopname = models.CharField(max_length=255)  # 商铺名
    add_time = models.DateField()  # 创建时间

    class Meta:
        db_table = 'shop_collect'
