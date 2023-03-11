from django.urls import path
from . import views

app_name='account'
urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('activate/<str:pk>/<str:token>',views.activate,name='activate'),
]
