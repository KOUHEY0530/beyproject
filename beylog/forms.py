from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Player, Beyblade
from .models import Match
from django.forms.models import inlineformset_factory
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']

    # BeybladeFormSet を作成 (Playerに紐づくBeyblade用)
BeybladeFormSet = inlineformset_factory(
    Player,           # 親モデル
    Beyblade,         # 子モデル
    fields=['name'],  # 登録するフィールド
    extra=1,          # 新規追加フォームをいくつ表示するか
    can_delete=True   # 削除機能をフォームに含める
)

class BeybladeForm(forms.ModelForm):
    class Meta:
        model = Beyblade
        fields = ['name', 'type']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['player1', 'player2', 'winner', 'date']

    player1 = forms.ModelChoiceField(queryset=Player.objects.all(), label='プレイヤー1')
    player2 = forms.ModelChoiceField(queryset=Player.objects.all(), label='プレイヤー2')
    winner  = forms.ModelChoiceField(queryset=Player.objects.all(), label='勝者')
    date = forms.DateField(widget=forms.SelectDateWidget, label='日付')

class PlayerBeybladeForm(forms.Form):
    player_name = forms.CharField(label='プレイヤー名', max_length=100)
    beyblade_name = forms.CharField(label='ベイブレード名', max_length=100)