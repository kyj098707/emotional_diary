from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views

router =  DefaultRouter()
router.register('diaries', views.DiaryViewSet)

app_name = "diary"
urlpatterns = [
    #path('', views.post_list),
    #path('<int:pk>', views.my_diary),
    path('intro/',views.intro_test,name='intro'),
    path('profile/<int:pk>/', views.profile_test,name="profile"),
    path('diary/new',views.diary_new,name="diary_new"),
    path('personal/personal_blog/',views.personal, name ='personal_blog'),
    path('api/',include(router.urls)),

]