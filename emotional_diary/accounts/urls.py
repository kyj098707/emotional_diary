from django.urls import path,include
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet
from . import views




app_name='account'

urlpatterns = [
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('activate/<str:pk>/<str:token>',views.activate,name='activate'),
    path('login/', views.login, name='login'),
    path('forget_password/',views.forget_password, name='forget_password'),
    path('reset_confirm/', views.reset_confirm, name='reset_confirm/'), 
    path('logout/',views.logout, name='logout'),
    path('statistics/',views.statistics_test, name='statistics'),
]
