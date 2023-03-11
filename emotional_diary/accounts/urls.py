from django.urls import path
from . import views
urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('forget_password/',views.forget_password, name='forget_password'),
    path('reset_confirm/', views.reset_confirm, name='reset_confirm/')
]
