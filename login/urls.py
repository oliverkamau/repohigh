from django.urls import path, re_path

from login import views

urlpatterns = [
    path(r'loginpage', views.login, name="loginpage"),
    path(r'userlogin', views.login_view, name="userlogin"),
    path(r'logout', views.logout, name="logout")

]
