from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_user, name="register"),
    path('student-register/', views.student_register, name="student-register"),
    path('userprofile/', views.userprofile, name="userprofile")

]
