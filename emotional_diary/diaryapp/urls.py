from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = "diary"
urlpatterns = [
    #path('', views.post_list),
    #path('<int:pk>', views.my_diary),
    path('intro/',views.intro_test,name='intro'),
    path('profile/<int:pk>/', views.profile_test,name="profile"),
    path('delete/',views.delete_qs,name="delete"),
    path('diary/new',views.diary_new,name="diary_new"),
]