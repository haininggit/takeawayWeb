"""takeawayWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path

# 主路由
urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('user/', include('mainapp.urls')),   # 添加用户路由
    re_path('order/', include('orderapp.urls')),  # 添加商户路由
    re_path('administe/', include('adminapp.urls')),  # 添加管理员路由
]
