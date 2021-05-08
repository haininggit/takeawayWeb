from django.db import models

# Create your models here.


# 商户表
class Shop(models.Model):
    shopname = models.CharField(max_length=255)  # 商铺名称
    mobile = models.CharField(max_length=255)  # 商铺电话
    password = models.CharField(max_length=255)  # 密码
    email = models.CharField(max_length=255)  # 邮箱
    status = models.IntegerField(default=0)  # 0代表未审核状态， 1代表已审核状态， 2代表已注销状态
    add_time = models.DateField()  # 创建时间

    class Meta:
        db_table = 'shop'


# 商户信息表
class ShopInfo(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='商铺')  # 商铺的ID
    contact_man = models.CharField(max_length=255)  # 联系人
    contact_mobile = models.CharField(max_length=255)  # 联系电话
    cateid = models.IntegerField(default=0)  # 门店类型
    begin_time = models.DateField(auto_now=True)  # 营业开始时间
    end_time = models.DateField(auto_now=True)  # 营业结束时间
    store_img = models.CharField(max_length=500)  # 店面图片
    instore_img = models.CharField(max_length=500)  # 店内图片
    logo_img = models.CharField(max_length=500)  # logo图片
    idCard_img = models.CharField(max_length=500)  # 身份证图片
    business_img = models.CharField(max_length=500)  # 营业执照图片
    license_img = models.CharField(max_length=500)  # 餐饮服务许可证
    address = models.CharField(max_length=255)  # 店面地址
    score = models.IntegerField(default=0)  # 平均评分
    box = models.IntegerField(default=0)  # 餐盒费用
    floor_send_cost = models.IntegerField(default=0)  # 起送费用

    class Meta:
        db_table = 'shop_info'


# 菜品信息表
class Food(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='商铺')  # 商铺的ID
    food_name = models.CharField(max_length=255)   # 食品名称
    tag = models.CharField(max_length=255)  # 标签    1.米饭、2.面食、3.火锅
    note = models.CharField(max_length=500)    # 描述
    cover_img = models.CharField(max_length=500)  # 食品封面图
    sell_price = models.IntegerField()   # 售价
    total_sales = models.IntegerField()   # 总销量
    month_sales = models.IntegerField()    # 月销量
    status = models.CharField(max_length=10)   # 状态
    add_time = models.DateField(auto_now=True)   # 创建时间

    class Meta:
        db_table = 'food'


# 订单表
class Order(models.Model):
    user_id = models.IntegerField()   # 用户Id
    shop_id = models.IntegerField()   # 商户Id
    pay_money = models.IntegerField()  # 需支付金额
    box_cost = models.IntegerField()  # 餐盒费
    send_cost = models.IntegerField()  # 配送费
    address = models.CharField(max_length=500)  # 配送地址
    note = models.CharField(max_length=500)  # 用户备注
    username = models.CharField(max_length=255)   # 用户名
    user_mobile = models.CharField(max_length=255)   # 用户联系电话
    shopname = models.CharField(max_length=255)  # 商铺名
    shop_mobile = models.CharField(max_length=255)   # 商铺联系电话
    deliver_name = models.CharField(max_length=255)  # 配送员姓名
    deliver_mobile = models.CharField(max_length=255)  # 配送员电话
    status = models.IntegerField()    # 订单状态
    add_time = models.DateField()  # 创建时间

    class Meta:
        db_table = 'order'


# 订单商品表
class OrderFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单表')   # 订单ID
    user_id = models.IntegerField()  # 用户Id
    shop_id = models.IntegerField()  # 商户Id
    food_id = models.IntegerField()  # 商品ID
    shopname = models.CharField(max_length=255)  # 商铺名
    food_name = models.CharField(max_length=255)  # 食品名称
    cover_img = models.CharField(max_length=500)  # 食品封面图
    sell_price = models.IntegerField()  # 售价
    tag = models.CharField(max_length=255)  # 标签    1.米饭、2.面食、3.火锅
    note = models.CharField(max_length=500)  # 描述
    add_time = models.DateField()  # 创建时间

    class Meta:
        db_table = 'order_food'

