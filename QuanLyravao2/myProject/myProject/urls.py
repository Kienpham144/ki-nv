from django.contrib import admin
from django.urls import path, include
from myApp.views import home_view, login_view, register_view, home3_view   # Import cả register_view
from myApp.urls import *
urlpatterns = [
    # url admin
    path('admin/', admin.site.urls), 
    # url home và maneager
    path('', include('myApp.urls')),      
]
