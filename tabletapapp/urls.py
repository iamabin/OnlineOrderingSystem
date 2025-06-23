from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("homepage/", views.login_view, name="homepage"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),  
    path("client/", views.client_order_view, name="client_order"),

    path("place_order/", views.place_order, name="place_order"),



]