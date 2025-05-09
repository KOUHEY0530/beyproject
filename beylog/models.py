from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'  # ここはユーザー名でログイン
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Beyblade(models.Model):
    player = models.ForeignKey(Player, related_name='beyblades', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_as_player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_as_player2')
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_won')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player1} vs {self.player2} - Winner: {self.winner}"
    
