from django.urls import path,include
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from accounts.views import UserViewSet, MyTokenObtainPairView,user_suggestion,my_profile_info
from . import views, views_rf
from .views import StatsRetrieveAPIView,UserRetrieveAPIView


app_name = 'account'


urlpatterns = [
    # page
    path('login_page/', views.login_page, name='login_page'),
    path('forget_password/', views.forget_password, name='forget_password'),

    path('signup/',views.SignupView.as_view(),name='signup'),
    path('activate/<str:pk>/<str:token>',views.activate,name='activate'),

    path('reset_confirm/', views.reset_confirm, name='reset_confirm/'),
    path('logout/',views.logout, name='logout'),
    path('statistics/',views.statistics_test, name='statistics'),

    # api
    path('follow/suggestion/',views.user_suggestion, name="api_user_suggestion"),
    path('user/myprofile/', views.my_profile_info, name="api_my_profile_info"),
    path('user/profile/info/', views.profile_info, name="api_profile_info"),
    path('user/profile/', views.profile, name="profile"),
    path('user/profile/<int:pk>/', views.profile_info, name="api_profile_detail"),
    path('user/<int:pk>/follow/', views.user_follow, name="follow"),
    path('user/<int:pk>/stats/', views.StatsRetrieveAPIView.as_view(), name="stats"),
    path('user/mypage/', views.my_page ,name="mypage"),
    path('user/<int:pk>/', views.UserRetrieveAPIView.as_view(), name="user_detail"),
    path('token/', MyTokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('signup/validate/', views.signup_validate, name="signup_validate"),
    
    # ====================================================
    # ====================================================
    # ====================================================
    
    
    path('service_login/', views_rf.login, name='login_page'),
    
    
    
    

]
