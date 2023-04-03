from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from .views import DiaryListCreateAPIView, comment_create, attach_tag, TagListCreateAPIView, DiaryRetrieveUpdateDestroyAPIView

# router = DefaultRouter()
# router.register(r'diary',DiaryViewSet)
# router.register(r'comment',CommentViewSet)


app_name = "diary"
urlpatterns = [
    #path('', views.post_list),
    #path('<int:pk>', views.my_diary),
    path('intro/',views.intro_test,name='intro'),
    path('profile/<int:pk>/', views.profile_test,name="profile"),
    path('personal/personal_blog/',views.personal, name ='personal_blog'),
    path('intro_test/',views.intro_test2,name='intro_2'),

    
    path('diary/',views.DiaryListCreateAPIView.as_view(),name="diary-list"),
    path('diary/<int:pk>/like/',views.diary_like,name='diary-like'),
    path('diary/<int:pk>/',views.DiaryRetrieveUpdateDestroyAPIView.as_view(),name="diary-detail"),
    path('diary/<int:pk>/comment/',views.comment_create,name="comment-create"),
    path('tag/',views.TagListCreateAPIView.as_view(),name="tag-create"),
    path('diary/<int:pk>/tag/',views.attach_tag,name="tag_attach"),
    #path('diary/<int:pk>/dislike/',views.diary_dislike,name='dislike'),
    
]