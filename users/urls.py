from django.urls import path
from users import views
from .views import logout_view, activate_account, activation_sent
from users.views import login_view, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from .views import render_terms, render_cookies, render_privacy, logout_view
# from .views import (
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.render_signup, name="render_signup"),
    path("cookies", render_cookies, name="render_cookies"),
    path("privacy", render_privacy, name="render_privacy"),
    path("terms", render_terms, name="render_terms"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('activation_sent/', activation_sent, name='activation_sent'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('logout/', logout_view, name='logout'),
]
