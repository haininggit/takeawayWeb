from django.db import models


# Create your models here.

# 管理员信息表
class AdminUser(models.Model):
    account = models.CharField(max_length=255)  # 登录账号
    password = models.CharField(max_length=255)  # 登录密码
    username = models.CharField(max_length=255)  # 用户名
    status = models.IntegerField()  # 1,在使用、2，已注销
    add_time = models.DateField()  # 创建时间

    class Meta:
        db_table = 'admin'

