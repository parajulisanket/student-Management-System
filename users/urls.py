# from django.urls import path
# from . import views

# urlpatterns = [
#     path('login/', views.LoginViewCustom.as_view(), name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('', views.dashboard, name='dashboard'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginViewCustom.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.signup_view, name='register'),
    path('', views.dashboard, name='dashboard'),
]