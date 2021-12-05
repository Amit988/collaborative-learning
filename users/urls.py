
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [

    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("delete-account/", views.deleteaccount, name="delete-account"),
    path("update-info/<slug:pk>/", views.UpdateInfo.as_view(), name="update-info"),
    path("verify/<str:auth_token>/", views.verify, name="verify"),

]