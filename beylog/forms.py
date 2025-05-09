from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory

from .models import User, Player, Beyblade, Match

# -------------------------
# ユーザー登録フォーム
# -------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# -------------------------
# プレイヤーフォーム
# -------------------------
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']
        labels = {
            'name': 'プレイヤー名',
        }

# -------------------------
# ベイブレード (Beyblade) 関連
# -------------------------

# 1. ベイブレード単体フォーム
class BeybladeForm(forms.ModelForm):
    class Meta:
        model = Beyblade
        fields = ['name']
        labels = {
            'name': 'ベイブレード名',
        }

# 2. プレイヤーに紐づくベイブレードFormSet (form=BeybladeForm 追加済み)

# 登録画面用 (extra=1 → 空欄フォーム1個)
BeybladeFormSetCreate = inlineformset_factory(
    Player,
    Beyblade,
    form=BeybladeForm,   # ← ラベル日本語化のため追加
    fields=['name'],
    extra=1,
    can_delete=False,
    validate_min=False,
    validate_max=False
)

# 編集画面用 (extra=0 → 既存データ分だけフォーム表示)
BeybladeFormSetUpdate = inlineformset_factory(
    Player,
    Beyblade,
    form=BeybladeForm,   # ← ラベル日本語化のため追加
    fields=['name'],
    extra=0,
    can_delete=False,
    validate_min=False,
    validate_max=False
)

# -------------------------
# 試合 (Match) フォーム
# -------------------------
class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['player1', 'player2', 'winner', 'date']

    player1 = forms.ModelChoiceField(queryset=Player.objects.all(), label='プレイヤー1')
    player2 = forms.ModelChoiceField(queryset=Player.objects.all(), label='プレイヤー2')
    winner  = forms.ModelChoiceField(queryset=Player.objects.all(), label='勝者')
    date = forms.DateField(
        widget=forms.TextInput(attrs={'id': 'datepicker'}),
        label='日付'
    )