from django.urls import path,include
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet
from . import views
from .views import StatsRetrieveAPIView,UserRetrieveAPIView


app_name = 'account'

urlpatterns = [
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('activate/<str:pk>/<str:token>',views.activate,name='activate'),
    path('login/', views.login, name='login'),
    path('forget_password/',views.forget_password, name='forget_password'),
    path('reset_confirm/', views.reset_confirm, name='reset_confirm/'), 
    path('logout/',views.logout, name='logout'),
    path('statistics/',views.statistics_test, name='statistics'),

    path('user/<int:pk>/follow/', views.user_follow, name="follow"),
    path('user/<int:pk>/stats/', views.StatsRetrieveAPIView.as_view(), name="stats"),
    path('user/mypage/', views.my_page ,name="mypage"),
    path('user/<int:pk>/', views.UserRetrieveAPIView.as_view(), name="user_detail"),
]
