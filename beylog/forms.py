from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError

from .models import User, Player, Beyblade, Match

# -------------------------
# ユーザー登録フォーム (←これ忘れてました)
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

class BeybladeForm(forms.ModelForm):
    class Meta:
        model = Beyblade
        fields = ['name']
        labels = {
            'name': 'ベイブレード名',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'required': 'required',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True

class RequiredBeybladeFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        count = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                name = form.cleaned_data.get('name')
                if name:
                    count += 1

        if count < 1:
            raise ValidationError('ベイブレードを少なくとも1つ入力してください。')

BeybladeFormSetCreate = inlineformset_factory(
    Player, Beyblade,
    form=BeybladeForm,
    formset=RequiredBeybladeFormSet,
    fields=['name'],
    extra=1,
    can_delete=False
)

BeybladeFormSetUpdate = inlineformset_factory(
    Player, Beyblade,
    form=BeybladeForm,
    formset=RequiredBeybladeFormSet,
    fields=['name'],
    extra=0,
    can_delete=False
)

# -------------------------
# 試合 (Match) フォーム
# -------------------------

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['player1', 'player2', 'winner', 'date']  # dateもあれば
        labels = {
            'player1': 'プレイヤー1',
            'player2': 'プレイヤー2',
            'winner': '勝者',
            'date': '日付',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 初期状態では winner を空にしておく
        self.fields['winner'].queryset = Player.objects.none()

        # POSTデータがある場合は player1 と player2 を使って winner を制限する
        if 'player1' in self.data and 'player2' in self.data:
            try:
                player1_id = int(self.data.get('player1'))
                player2_id = int(self.data.get('player2'))
                self.fields['winner'].queryset = Player.objects.filter(id__in=[player1_id, player2_id])
            except (ValueError, TypeError):
                pass  # 無効な入力なら何もしない

        # インスタンス編集時（match_update）も対応
        elif self.instance.pk:
            players = [self.instance.player1, self.instance.player2]
            self.fields['winner'].queryset = Player.objects.filter(id__in=[p.id for p in players if p])