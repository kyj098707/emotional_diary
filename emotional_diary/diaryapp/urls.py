from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from . import views_api as api
from .views_api import DiaryListCreateAPIView, comment_create, attach_tag, TagListCreateAPIView, DiaryRetrieveUpdateDestroyAPIView



app_name = "diary"

urlpatterns = [
    
    path('home/',views.home,name='home'),
    path('social/',views.social,name='social'),
    path('profile/', views.post,name="post"),
    
    path('personal/personal_blog/',views.personal_page, name ='personal_blog'),
    path('newsfeed/list', views.newsfeed_list, name="newsfeed_list"),
    path('newsfeed/<int:pk>/test', views.newsfeed_test, name="newsfeed_test"),

    #api
    path('diary/mylist/',api.my_diary_list,name="my-diary-list"),
    path('diary/', api.DiaryListCreateAPIView.as_view(), name="diary-list"),
    path('diary/<int:pk>/list/', api.user_diary_list, name="user-diary-list"),
    path('diary/<int:pk>/like/',api.diary_like,name='diary-like'),
    path('diary/<int:pk>/',api.DiaryRetrieveUpdateDestroyAPIView.as_view(),name="diary-detail"),
    path('diary/<int:pk>/comment/',api.comment_create,name="comment-create"),
    path('tag/',api.TagListCreateAPIView.as_view(),name="tag-create"),
    path('diary/<int:pk>/tag/',api.attach_tag,name="tag_attach"),
    #path('diary/<int:pk>/dislike/',api.diary_dislike,name='dislike'),
    
]