
from django.urls import path, re_path

from orderapp import views


urlpatterns = [
    re_path(r'^login/$', views.login.as_view()),
    re_path(r'^register/$', views.register.as_view()),
    re_path(r'^CRUDFoods/$', views.CRUDFoods.as_view()),
    re_path(r'^getOrder/$', views.getOrder.as_view()),
]

