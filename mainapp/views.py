import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse, QueryDict

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from mainapp.models import UserEntity, Address
from mainapp.serializer import UserSerializer, ShopFoodsSerializer, AddressSerializer, ShopInfosSerializer
from orderapp.models import Shop, Order
from django.core.cache import cache

# 登录
from orderapp.serializer import OrderAndFoodSerializer
from utils.ResBody import failed, successful


class login(APIView):
    """
    用户的登录
    """

    # 获取所有用户
    def get(self, request):
        users = UserEntity.objects.all()
        users = UserSerializer(users, many=True)
        return JsonResponse(users.data, safe=False)

    # 进行登录验证
    def post(self, request):
        """
        登录成功，存储cookies
        :param request:
        :return:
        """
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        try:
            user = UserEntity.objects.get(mobile=mobile, password=password)
            user = UserSerializer(user)
            # response = HttpResponse()
            # response.set_cookie('id', user.id)
            # response.set_cookie('username', bytes(user.username, 'utf-8').decode('ISO-8859-1'))
        except:
            # return Response({'error': "用户名或密码错误！"})
            return Response(failed("用户名或密码错误！"))
        return Response(successful(user.data))


# 注册
class register(APIView):
    """
    进行用户的注册
    """

    # def get(self, request):
    #     # 返回注册的页面
    #     return render(request, 'regiest.html', locals())

    def post(self, request):
        # 1.获取参数
        data = request.body.decode()
        data_dict = json.loads(data)
        # 2.验证参数
        ser = UserSerializer(data=data_dict)
        ser.is_valid()
        if ser.errors.__len__() != 0:
            return JsonResponse(ser.errors)
        # 3.保存数据
        ser.save()
        # 4.返回数据
        return JsonResponse(ser.data, safe=False)


# 主页数据展示
class homepage(APIView):
    """
    获取商铺以及商铺数据
    主页
    """

    def get(self, request):
        shops = Shop.objects.filter(status=1)
        ser = ShopInfosSerializer(shops, many=True)
        return Response(successful(ser.data))


# 店铺详情页
class shopFoodsInfo(APIView):
    """
    获取单个商铺的信息以及菜单
    """

    def get(self, request):
        id = request.GET.get('id')
        # print(id)
        try:
            shop = Shop.objects.get(id=id)
            ser = ShopFoodsSerializer(shop)
            return Response(successful(ser.data))
        except:   # {'error': "商铺不存在！"}
            return Response(failed("商铺不存在！"))


# 查询所有地址
class CRUDAddress(APIView):
    """
    查询、新增、修改、删除地址
    """

    # 查询用户所有地址
    def get(self, request):
        user_id = request.GET.get("id")
        address = Address.objects.filter(user_id=user_id)
        address = AddressSerializer(address, many=True)
        return JsonResponse(address.data, safe=False)

    # 新增用户数据
    def post(self, request):
        # 1.获取参数
        data = request.body.decode()
        data_dict = json.loads(data)
        # 2.验证参数
        ser = AddressSerializer(data=data_dict)
        ser.is_valid()
        if ser.errors.__len__() != 0:
            return JsonResponse(ser.errors)
        # 3.保存数据
        ser.save()
        # 4.返回数据
        return JsonResponse(ser.data, safe=False)

    # 删除地址信息
    def delete(self, request):
        id = request.GET.get("id")
        try:
            address = Address.objects.get(id=id)
            address.delete()
            return JsonResponse({'msg': "删除成功！"}, safe=False)
        except:
            return JsonResponse({'error': "该地址不存在或已被删除！"}, safe=False)

    # 修改数据
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
            address = Address.objects.get(id=id)
            ser = AddressSerializer(address, data=data_dict)
            ser.is_valid()
            if ser.errors.__len__() != 0:
                return JsonResponse(ser.errors)
            # 3.保存数据
            ser.save()
            # 4.返回数据
            return JsonResponse(ser.data, safe=False)
        except:
            return JsonResponse({'error': "该地址不存在或已被删除！"}, safe=False)


# 添加购物车
class addShopCart(APIView):
    """
    购物车的增删改查
    """

    # 查询
    def get(self, request):
        user_id = request.GET.get(id)
        order_list = cache.get(user_id)
        try:
            if cache.has_key(user_id):  # 缓存中有数据则返回
                food_list = cache.get(user_id)
                return JsonResponse(food_list, safe=False)
            else:  # redis里面若没有，则在数据库中返回
                order = Order.objects.get(user_id=user_id, add_time=datetime.today())
                order_food_list = OrderAndFoodSerializer(order)
                return JsonResponse(order_food_list.data, safe=False)
        except:
            return JsonResponse("没有订单，去添加订单吧！", safe=False)

    # 添加到购物车
    def post(self, request):
        # cache.set("key", 'value', 60*60)
        user_id = request.COOKIES.get('id')
        if not id:
            # 未登录,进行处理
            return JsonResponse("未登录，请立即登录！")
        food_id = request.POST.get('id')
        # 3.保存数据在Redis中
        if cache.has_key(user_id):
            list = [food_id]
            cache.set(user_id, list)
        else:
            cache.set((list(cache.get(user_id))).append(food_id))
        # 4.返回数据
        return JsonResponse("添加成功", safe=False)

    # 删除购物车里面的商品
    def delete(self, request):
        user_id = request.COOKIES.get('id')
        id = request.GET.get("id")
        food_list = list(cache.get(user_id))
        food_list.remove(id)
        cache.set((list(cache.get(user_id))).append(food_list))



class test(APIView):
    def get(self, request):
        id = request.GET.get('id')
        address = Address.objects.get(id=id)
        return JsonResponse(AddressSerializer(address).data, safe=False)
