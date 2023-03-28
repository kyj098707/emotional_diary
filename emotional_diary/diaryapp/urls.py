from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views


app_name = "diary"
urlpatterns = [
    #path('', views.post_list),
    #path('<int:pk>', views.my_diary),
    path('intro/',views.intro_test,name='intro'),
    path('profile/<int:pk>/', views.profile_test,name="profile"),
    path('diary/new',views.diary_new,name="diary_new"),
    path('personal/personal_blog/',views.personal, name ='personal_blog'),
    #path('diary/',views.handle_diary,name="handle_diary"),
    path('intro_test/',views.intro_test2,name='intro_2'),
    path('user/follow/',views.user_follow,name='follow'),
    path('user/unfollow/',views.user_unfollow,name='unfollow'),
    path('diary/like/',views.diary_like,name='like'),
    path('diary/dislike/',views.diary_dislike,name='dislike'),
    
]