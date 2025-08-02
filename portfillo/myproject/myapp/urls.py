from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.register,name='register'),
    path('login',views.login,name='login'),
    path('index',views.index,name='index'),
    path('logout',views.logout_view,name='logout'),
]