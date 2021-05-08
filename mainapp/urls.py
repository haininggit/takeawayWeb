from django.urls import re_path
from django.conf import settings
from django.conf.urls. static import static
from mainapp import views

urlpatterns = [
    re_path(r'^login/$', views.login.as_view()),
    re_path(r'^register/$', views.register.as_view()),
    re_path(r'^homepage/$', views.homepage.as_view()),
    re_path(r'^shopFoodsInfo/$', views.shopFoodsInfo.as_view()),
    re_path(r'^CRUDAddress/$', views.CRUDAddress.as_view()),
    re_path(r'^test/$', views.test.as_view()),
] + static (settings.STATIC_URL, document_root = settings.STATIC_ROOT)
