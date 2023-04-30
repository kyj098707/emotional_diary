from django.urls import path,include
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from accounts.views_api import UserViewSet, MyTokenObtainPairView,user_suggestion, StatsRetrieveAPIView,UserRetrieveAPIView
from . import views
from . import views_api as api


app_name = 'account'


urlpatterns = [
    # page
    path('login/', views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('activate/<str:pk>/<str:token>',views.activate,name='activate'),
    

    # api
    path('signup/',api.SignupView.as_view(),name='signup'),
    path('signup/validate/', api.signup_validate, name="signup_validate"),
    
    path('follow/suggestion/',api.user_suggestion, name="api_user_suggestion"),
    
    #메인 인포단과 팔로우십 인포단을 나눕니다.
    #이렇게 하면 부분 html을 쓸 필요 없이 단순 html 컴포넌트로 해결 가능.
    path('user/myprofile_mn_info/', api.my_profile_mn_info, name="api_my_profile_mn_info"), #메인 정보 요청
    path('user/myprofile_fw_info/', api.my_profile_fw_info, name="api_my_profile_fw_info"), #팔로우 관련 정보 요청
    
    path('user/profile/info/', api.profile_info, name="api_profile_info"),
    path('user/profile/', api.profile, name="profile"),
    path('user/profile/<int:pk>/', api.profile_info, name="api_profile_detail"),
    path('user/<int:pk>/follow/', api.user_follow, name="follow"),
    path('user/<int:pk>/stats/', api.StatsRetrieveAPIView.as_view(), name="stats"),
    path('user/mypage/', api.my_page ,name="mypage"),
    path('user/<int:pk>/', api.UserRetrieveAPIView.as_view(), name="user_detail"),
    path('user/followlist/',api.my_follower_list,name="api-my-followlist"),
    path('user/followlist/<int:pk>/', api.user_follower_list, name="api-user-followlist"),
    # ====================================================
    # ====================================================
    # ====================================================
    
    # especially for..
    path('token/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify"),
    
    
    

]
