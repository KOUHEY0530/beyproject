from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # -------------------- 基本ページ --------------------
    path('', views.home, name='home'),

    # -------------------- 認証関係 --------------------
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # -------------------- プレイヤー管理 --------------------
    path('player/list/', views.player_list, name='player_list'), # 残す
    path('player/stats/', views.player_stats, name='player_stats'), # 残す
    path('player/update/<int:pk>/', views.player_update, name='player_update'), # 残す
    path('player/delete/<int:pk>/', views.PlayerDeleteView.as_view(), name='player_delete'), #残す

    # -------------------- プレイヤー・ベイブレード管理 --------------------
    path('player_beyblade/create/', views.player_beyblade_create, name='player_beyblade_create'), # 残す

    # -------------------- 対戦管理 --------------------
    path('match/create/', views.match_create, name='match_create'), # 残す
    path('match/<int:pk>/edit/', views.match_update, name='match_update'), #　残す
    path('match/<int:pk>/delete/', views.match_delete, name='match_delete'), #　残す
    path('match/list/', views.match_list, name='match_list'), # 残す
]