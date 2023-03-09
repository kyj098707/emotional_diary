from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.post_list),
    #path('<int:pk>', views.my_diary),
    path('intro/',views.intro_test,name='intro'),
]