from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('accounts/registration/', views.register, name='registration'),
    #path('accounts/registration/', views.RegisterView.as_view(), name='registration'),
    path('accounts/login', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout', views.logout_view, name='logout'),
    path('welcome/', views.welcome, name='welcome'),
    path('users/', views.user_list, name='user_list'),
]
