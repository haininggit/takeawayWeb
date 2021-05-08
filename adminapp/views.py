import json

from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from adminapp.models import AdminUser
from mainapp.serializer import ShopInfosSerializer
from orderapp.models import Shop
from utils.ResBody import successful, failed


class login(APIView):
    """
    进行用户的登录
    """
    # 进行登录验证
    def post(self, request):
        # 接受前端数据
        data = request.data
        # print(data)
        account = data['account']
        password = data['password']
        # 查询
        print(str(account)+" "+str(password))
        try:
            account = AdminUser.objects.get(account=account, password=password)
            data = {'msg': "登录成功！"}
            return Response(successful(data))
        except:
            data = {"用户名或密码错误！"}
            return Response(failed(data))


class verifyShop(APIView):
    """
    商家的审核
    """
    # 查询所有未审核的商家
    def get(self, request):
        shops = Shop.objects.filter(status=0)
        ser = ShopInfosSerializer(shops, many=True)
        return Response(successful(ser.data))

    # 审核
    def put(self, request):
        # 获取id
        id = request.GET.get("id")  # 获取传递参数
        # print(id)
        try:
            shop = Shop.objects.get(id=id)
            shop.status = 1
            shop.save()
            data = {"msg":"审核通过！"}
            return Response(successful(data))
        except:
            return Response(failed("商户不存在或已被删除！"))




