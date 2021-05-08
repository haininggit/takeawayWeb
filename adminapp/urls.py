from django.urls import path, re_path

from adminapp import views

urlpatterns = [
    re_path(r'^login/$', views.login.as_view()),
    re_path(r'^verifyShop/$', views.verifyShop.as_view()),
]
