from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('player/create/', views.player_create, name='player_create'),
    path('beyblade/create/', views.beyblade_create, name='beyblade_create'),
    path('match/create/', views.match_create, name='match_create'),
    path('match/list/', views.match_list, name='match_list'),
]