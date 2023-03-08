from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.post_list),
    #path('<int:pk>', views.my_diary),
    path('login/',LoginView.as_view(template_name='__01_account/login_form.html'),name='login'),
    path('profile/', views.profile, name="profile"),
]