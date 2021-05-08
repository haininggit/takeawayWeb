import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render

# Create your views here.


# 商户登录
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from orderapp.models import Shop, ShopInfo, Food, Order
from orderapp.serializer import ShopSerializer, ShopInfoSerializer, FoodSerializer, OrderAndFoodSerializer
from utils.ResBody import successful, failed


class login(APIView):
    """
    商铺的登录
    """

    # 进行登录验证 并实现websoket
    def post(self, request):
        # data = request.data
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        try:
            shop = Shop.objects.get(mobile=mobile, password=password)
            shop = ShopSerializer(shop)

            # response = HttpResponse()
            # response.set_cookie('id', user.id)
            # response.set_cookie('username', bytes(user.username, 'utf-8').decode('ISO-8859-1'))
        except:
            # return Response({'error': "用户名或密码错误！"})
            return Response(failed("用户名或密码错误！"))
        return Response(successful(shop.data))


class register(APIView):
    """
    进行商户的注册
    下面的代码注册存在问题
    商户的注册
    """

    def post(self, request):
        # 1.获取参数
        data = request.body.decode()
        data_dict = json.loads(data)
        # 2.验证参数
        ser = ShopSerializer(data=data_dict)
        ser.is_valid(raise_exception=True)
        # 3.获取验证的数据
        # shop = Shop(
        #     shopname=shopName,
        #     mobile=mobile,
        #     password=password,
        #     email=email,
        #     status=0,
        #     add_time=datetime.now()
        # )
        # 返回验证结果
        return JsonResponse(ser.errors)


class CRUDFoods(APIView):
    """
    商家菜单的增删改查
    """
    # 查询该商户所有产品
    def get(self, request):
        shop_id = request.GET.get('id')
        foods = Food.objects.filter(shop=shop_id)
        return JsonResponse(FoodSerializer(foods, many=True).data, safe=False)

    # 增加产品food
    def post(self, request):
        # 1.获取参数
        data = request.body.decode()
        data_dict = json.loads(data)
        # 2.验证参数
        ser = FoodSerializer(data=data_dict)
        ser.is_valid()
        if ser.errors.__len__() != 0:
            return JsonResponse(ser.errors)
        # 3.保存数据
        ser.save()
        # 4.返回数据
        return JsonResponse(ser.data, safe=False)

    # 修改产品
    def put(self, request):
        # 获取id
        put = QueryDict(request.body)
        put_str = list(put.items())[0][0]  # 将获取的QueryDict对象转换为str 类型
        put_dict = eval(put_str)  # 将str类型转换为字典类型
        id = put_dict.get("id")  # 获取传递参数

        # 1.获取参数
        data = request.body.decode()
        data_dict = json.loads(data)
        # print(id)
        # 2.验证参数  15991642732  15901642732
        try:
            food = Food.objects.get(id=id)
            ser = FoodSerializer(food, data=data_dict)
            ser.is_valid()
            if ser.errors.__len__() != 0:
                return JsonResponse(ser.errors)
            # 3.保存数据
            ser.save()
            # 4.返回数据
            return JsonResponse(ser.data, safe=False)
        except:
            return JsonResponse({'error': "该产品不存在或已被删除！"}, safe=False)

    # 删除产品
    def delete(self, request):
        id = request.GET.get('id')
        try:
            food = Food.objects.get(id=id)
            food.delete()
            return JsonResponse({'msg': "删除成功！"}, safe=False)
        except:
            return JsonResponse({'error': "该产品不存在或已被删除！"}, safe=False)


class getOrder(APIView):
    """
    该商家订单的查找
    """
    def get(self, request):
        id = request.GET.get("id")
        try:
            order = Order.objects.filter(shop_id=id, status=0, add_time=datetime.today())
            order = OrderAndFoodSerializer(order, many=True)
            return Response(successful(order.data))
        except:
            return Response(failed("未产生订单"))

    # jiedan
    def put(self, request):
        data = request.data
        id = data['orderId']
        # print(data)
        try:
            order = Order.objects.get(id=id)
            order.status = 1
            order.save()
        except:
            return Response(failed("接单失败"))
        return Response(successful("接单成功"))
