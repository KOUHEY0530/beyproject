from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Player, Beyblade
from .models import Match

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']

class BeybladeForm(forms.ModelForm):
    class Meta:
        model = Beyblade
        fields = ['name', 'type']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('player1', 'player2', 'winner', 'date')