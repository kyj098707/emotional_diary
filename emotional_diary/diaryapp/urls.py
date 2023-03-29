from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from diaryapp.views import DiaryListAPIView,DiaryRetrieveAPIView,CommentCreateAPIView

# router = DefaultRouter()
# router.register(r'diary',DiaryViewSet)
# router.register(r'comment',CommentViewSet)


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
    
    # path('profile/',views.user_follow,name='profile'),
    # path('profile/<int:pk>',views.user_follow,name='profile_detail'),
    # path('profile/<int:pk>/follow/',views.user_follow,name='follow'),
    # path('profile/<int:pk>/unfollow/',views.user_unfollow,name='unfollow'),

    #path('diary/',views.diary_like,name='diary'),
    path('diary/',views.DiaryListAPIView.as_view(),name="diary-list"),
    path('diary/<int:pk>/like/',views.diary_like,name='diary-like'),
    path('diary/<int:pk>/',views.DiaryRetrieveAPIView.as_view(),name="diary-list"),
    path('comment/',views.CommentCreateAPIView.as_view(),name="comment-list"),
    #path('diary/<int:pk>/dislike/',views.diary_dislike,name='dislike'),
    
]