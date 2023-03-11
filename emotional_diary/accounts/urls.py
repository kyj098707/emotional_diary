from django.urls import path,include
from . import views

app_name='account'
urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('activate/<str:pk>/<str:token>',views.activate,name='activate'),
    path('login/', views.login, name='login'),
    path('forget_password/',views.forget_password, name='forget_password'),
    path('reset_confirm/', views.reset_confirm, name='reset_confirm/'),
    path('logout/',views.logout, name='logout'),
    path('send_mail/',views.send_email_test, name='send'),
]
