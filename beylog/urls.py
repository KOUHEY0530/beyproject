from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('player/create/', views.player_create, name='player_create'),
    path('beyblade/create/', views.beyblade_create, name='beyblade_create'),
    path('match/create/', views.match_create, name='match_create'),
    path('match/list/', views.match_list, name='match_list'),
    path('player/list/', views.player_list, name='player_list'),
    path('player_beyblade/create/', views.player_beyblade_create, name='player_beyblade_create'),
    path('player_beyblade/<int:player_id>/update/', views.player_beyblade_update, name='player_beyblade_update'),
    path('player_beyblade/<int:player_id>/delete/', views.player_beyblade_delete, name='player_beyblade_delete'),
    path('player/<int:player_id>/edit/', views.player_beyblade_update, name='player_beyblade_update'),
    path('player/<int:player_id>/delete/', views.player_beyblade_delete, name='player_beyblade_delete'),
]