# 自定义序列化器
import re
from abc import ABC
from datetime import datetime

from rest_framework import serializers

# 用户注册时候进行用户的验证
from mainapp.models import UserEntity, Address

# 用户序列化器
from orderapp.serializer import ShopInfoSerializer, FoodSerializer


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, min_length=2)
    mobile = serializers.CharField(max_length=255, min_length=11)
    password = serializers.CharField(max_length=255, min_length=6)
    email = serializers.CharField(max_length=255)
    gender = serializers.CharField()
    # 只参与返回序列化
    id = serializers.IntegerField(read_only=True)
    wallet = serializers.CharField(read_only=True)
    user_img = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    add_time = serializers.DateField(read_only=True)

    # 进行验证其他注册数据的正确性
    def validate(self, attrs):
        # 验证电话是否重复
        try:
            mobile = UserEntity.objects.get(mobile=attrs['mobile'])
            if mobile is not None:
                raise serializers.ValidationError('电话已注册！')
        except UserEntity.DoesNotExist:
            pass

        # 验证email是否重复
        try:
            email = UserEntity.objects.get(email=attrs['email'])
            if email is not None:
                raise serializers.ValidationError('email已注册！')
        except UserEntity.DoesNotExist:
            pass

        # 检验注册格式是否正确
        if len(attrs['email']) > 7 and re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                                                attrs['email']) is not None:
            if len(attrs['password']) >= 6:
                if re.match('^(13(7|8|9|6|5|4)|17(0|8|3|7)|18(2|3|6|7|9)|15(3|5|6|7|8|9))\d{8}$',
                            attrs['mobile']) is not None:
                    return attrs
                else:
                    raise serializers.ValidationError("电话号码格式不正确！")
            else:
                raise serializers.ValidationError("密码长度不能少于6！")
        else:
            raise serializers.ValidationError("email格式不正确！")

    def create(self, validated_data):
        user = UserEntity.objects.create(
            **validated_data,
            wallet=0,
            status=0,
            add_time=datetime.today())
        return user


# 商户序列化器（前端页面返回的）
class ShopInfosSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    shopname = serializers.CharField()
    email = serializers.CharField()
    status = serializers.IntegerField()
    add_time = serializers.DateField()

    shopinfo_set = ShopInfoSerializer(many=True)


# 单个商户序列化器
class ShopFoodsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    shopname = serializers.CharField()

    food_set = FoodSerializer(many=True)


# 添加地址
class AddressSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=255)
    mobile = serializers.CharField()
    address = serializers.CharField(max_length=255)
    default = serializers.IntegerField()
    tag = serializers.CharField(max_length=255)

    # 只支持接受
    user_id = serializers.IntegerField(write_only=True)

    # 只支持返回序列化
    status = serializers.IntegerField(read_only=True)

    # 验证电话号码是否正确
    def validate(self, attrs):
        if re.match('^(13(7|8|9|6|5|4)|17(0|8|3|7)|18(2|3|6|7|9)|15(3|5|6|7|8|9))\d{8}$',attrs['mobile']) is not None:
            return attrs
        else:
            raise serializers.ValidationError("电话号码格式不正确！")

    # 创建并存储
    def create(self, validated_data):
        address = Address.objects.create(
            **validated_data,
            status=0,
        )
        return address

    # 更新数据
    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.gender = validated_data['gender']
        instance.mobile = validated_data['mobile']
        instance.address = validated_data['address']
        instance.default = validated_data['default']
        instance.tag = validated_data['tag']
        instance.save()
        return instance







