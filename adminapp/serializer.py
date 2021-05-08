from rest_framework import serializers


# 自定义序列化器

class AdminSerializer(serializers.Serializer):
    # 序列化返回的字段
    account = serializers.CharField(max_length=255, min_length=2)  # 登录账号  ,最大255，最小2，以下类似
    password = serializers.CharField(max_length=255, min_length=6)  # 登录密码
    username = serializers.CharField(max_length=255, min_length=2, required=False)  # 用户名

