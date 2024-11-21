# myProject/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Trang đăng nhập
    path('', views.home_view, name='home'),          # Trang chủ
    path('', view.home3_view, name='home3'),
]
