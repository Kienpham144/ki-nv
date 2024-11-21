from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
  
    path('register/', views.register_view, name='register'),
    path('register_guide/', views.register_guide, name='register_guide'),
    
    # Home pages
    path('home/', views.home_view, name='home'),
    path('home3/', views.home_view, name='home3'),

    # Admin pages
    path('waiting_list/', views.waiting_list, name='waiting'),
    path('diary_form/', views.diary_form, name='diary_form'),
    path('diary_list/', views.diary_list, name='diary_list'),

    # Rules and Information
    path('rules/', views.noiquy_ra_ngoai_view, name='rules'),  # Nội Quy
    path('news/', views.news_list, name='news'),              # Danh sách tin tức
    path('create/', views.create_news, name='create_news'),   # Trang đăng tin tức
    
    # Game
    path('game/', views.game, name='game'),

    # Miscellaneous
    path('base/', views.home_view, name='base'),
    path('base3/', views.home_view, name='base3'),


    path('ds_lop/', views.ds_lop_list, name='ds_lop_list'),
    path('add_ds_lop/', views.add_ds_lop, name='add_ds_lop'),
    path('ds_lop/delete/<int:pk>/', views.delete_ds_lop, name='delete_ds_lop'),


 
]

    

