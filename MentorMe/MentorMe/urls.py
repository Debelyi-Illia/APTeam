"""
URL configuration for MentorMe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.showHomePage, name="home"),
    path("user_profile/", views.UserView, name="user_profile"),
    path('login/', views.LoginView, name='login'),
    path('register/', views.RegisterView, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('search/', views.search_advertisements, name='search'),
    path('ad/', views.AdView, name='ad'),
    path('create_ad/', views.create_ad, name='create_ad'),

]
