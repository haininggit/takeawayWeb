from datetime import datetime

from rest_framework import serializers


# 自定义序列化器
from orderapp.models import Food, Order


# 商铺序列化器
class ShopSerializer(serializers.Serializer):
    shopname = serializers.CharField(max_length=255, min_length=2)
    mobile = serializers.CharField(max_length=255, min_length=5)
    password = serializers.CharField(max_length=255, min_length=6)
    email = serializers.CharField(max_length=255)

    # 只参与返回序列化
    id = serializers.IntegerField(read_only=True)
    status = serializers.IntegerField(read_only=True)
    add_time = serializers.DateField(read_only=True)


    # 多个字段进行验证
    def validate(self, attrs):
        if attrs['mobile']:
            return True
        else:
            raise serializers.ValidationError("数据验证错误")


# food序列化器
class FoodSerializer(serializers.Serializer):
    """
    菜品序列化器
    """
    food_name = serializers.CharField(max_length=255)
    tag = serializers.CharField(max_length=255)
    note = serializers.CharField(max_length=500)
    cover_img = serializers.CharField(max_length=500, required=False)
    sell_price = serializers.IntegerField()

    # 只参与接受序列化
    shop = serializers.IntegerField(write_only=True, required=False)

    # 只参与返回序列化
    id = serializers.IntegerField(read_only=True)
    total_sales = serializers.IntegerField(read_only=True)
    month_sales = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    add_time = serializers.DateField(read_only=True)
    # shop_id = serializers.IntegerField(read_only=True)

    # 简单验证参数
    def validate(self, attrs):
        return attrs

    # 创建保存
    def create(self, validated_data):
        food = Food.objects.create(
            shop_id=validated_data['shop'],
            food_name=validated_data['food_name'],
            tag=validated_data['tag'],
            note=validated_data['note'],
            cover_img=validated_data['cover_img'],
            sell_price=validated_data['sell_price'],
            total_sales=0,
            month_sales=0,
            status=0,
            add_time=datetime.today())
        return food

    # 修改
    def update(self, instance, validated_data):
        instance.food_name = validated_data['food_name']
        instance.tag = validated_data['tag']
        instance.note = validated_data['note']
        instance.sell_price = validated_data['sell_price']
        instance.save()
        return instance


# 商户信息序列化器
class ShopInfoSerializer(serializers.Serializer):
    """
    商户信息序列化器
    """
    contact_man = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    contact_mobile = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    cateid = serializers.IntegerField()
    begin_time = serializers.DateField()
    end_time = serializers.DateField()
    store_img = serializers.CharField(max_length=500)
    instore_img = serializers.CharField(max_length=500)
    logo_img = serializers.CharField(max_length=500)
    address = serializers.CharField(max_length=255)
    score = serializers.IntegerField()
    box = serializers.IntegerField()
    floor_send_cost = serializers.IntegerField()

    # 只负责接受序列化
    idCard_img = serializers.CharField(max_length=500,write_only=True)
    business_img = serializers.CharField(max_length=500, write_only=True)
    license_img = serializers.CharField(max_length=500, write_only=True)
    shop_id = serializers.IntegerField(write_only=True)

    # 只负责返回序列化
    id = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        return attrs


# 订单商品序列化器
class OrderFoodSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    food_id = serializers.IntegerField()
    shopname = serializers.CharField()
    food_name = serializers.CharField()
    cover_img = serializers.CharField()
    sell_price = serializers.IntegerField()
    tag = serializers.CharField()
    note = serializers.CharField()
    add_time = serializers.DateField()


# 订单序列化器
class OrderAndFoodSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    shop_id = serializers.IntegerField()
    pay_money = serializers.IntegerField()
    address = serializers.CharField()
    note = serializers.CharField()
    deliver_name = serializers.CharField()
    deliver_mobile = serializers.CharField()

    # 只参与返回序列化
    id = serializers.IntegerField(read_only=True)
    box_cost = serializers.IntegerField(read_only=True)
    send_cost = serializers.IntegerField(read_only=True)
    shopname = serializers.CharField(read_only=True)
    shop_mobile = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    user_mobile = serializers.CharField(read_only=True)
    status = serializers.IntegerField(read_only=True)
    add_time = serializers.DateField(read_only=True)

    orderfood_set = OrderFoodSerializer(many=True, read_only=True)





