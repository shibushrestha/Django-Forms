from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_user, name="register"),
    path('student-register/', views.student_register, name="student-register"),
    path('userprofile/', views.userprofile, name="userprofile"),

    path('user_registration/', views.user_registration, name='registration'),

    path('add_students/', views.add_students, name='add-students'),

    path('add_userprofile/', views.add_userprofile, name='add-userprofile'),

]
