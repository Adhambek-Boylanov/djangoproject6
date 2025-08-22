from django.urls import path
from .views import *
urlpatterns = [
    path("", login_view, name="login"),
    path("home/",index, name="home"),
    path('add_brand/',add_brand,name='add_brand'),
    path('add_car/',add_car,name = 'add_car'),
    path('brand_detail/<int:pk>/', brand_detail, name='brand_detail'),
    path('detail_car/<int:pk>/',detail_car,name = 'detail_car'),
    path('download_car_pdf/<int:pk>/', download_car_pdf, name='download_car_pdf'),
]