from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView, UpdateView
from django.db.models import Q

from .forms import CustomUserCreationForm, PlayerForm, BeybladeFormSetCreate, BeybladeFormSetUpdate
from .models import Player, Beyblade, Match
from .forms import MatchForm
from django.urls import reverse

# -------------------------
# ホーム & 認証
# -------------------------

@login_required
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# -------------------------
# プレイヤー (Player)
# -------------------------

@login_required
def player_list(request):
    players = Player.objects.filter(user=request.user)
    return render(request, 'player_list.html', {'players': players})


@login_required
def player_update(request, pk):
    player = get_object_or_404(Player, pk=pk, user=request.user)

    if request.method == 'POST':
        player_form = PlayerForm(request.POST, instance=player)
        formset = BeybladeFormSetCreate(request.POST, instance=player)

        if player_form.is_valid() and formset.is_valid():
            player = player_form.save()

            formset.instance = player
            instances = formset.save(commit=False)
            for instance in instances:
                instance.player = player
                instance.save()

            return redirect('player_list')
    else:
        player_form = PlayerForm(instance=player)
        formset = BeybladeFormSetUpdate(instance=player)

    return render(request, 'player_beyblade_form.html', {
        'title': 'プレイヤー編集',
        'player_form': player_form,
        'formset': formset,
        'player': player
    })

@method_decorator(login_required, name='dispatch')
class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'player_confirm_delete.html'
    success_url = reverse_lazy('player_list')

    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

# -------------------------
# 統計 (Stats)
# -------------------------

@login_required
def player_stats(request):
    players = Player.objects.filter(user=request.user)
    stats = []

    for player in players:
        total_matches = Match.objects.filter(Q(player1=player) | Q(player2=player)).count()
        wins = Match.objects.filter(winner=player).count()
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0

        stats.append({
            'player': player,
            'total_matches': total_matches,
            'wins': wins,
            'win_rate': round(win_rate, 2),
        })

    return render(request, 'player_stats.html', {'stats': stats})

@login_required
def player_beyblade_create(request):
    if request.method == 'POST':
        player_form = PlayerForm(request.POST)
        formset = BeybladeFormSetCreate(request.POST)

        if player_form.is_valid() and formset.is_valid():
            player = player_form.save(commit=False)
            player.user = request.user
            player.save()

            formset.instance = player
            # 空欄フォーム除外して保存
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.name:  # ← 空欄なら保存しない
                    instance.player = player
                    instance.save()

            return redirect('player_list')
        else:
            # デバッグ出力 (一旦見る用)
            print("player_form errors:", player_form.errors)
            print("formset errors:", formset.errors)

    else:
        player_form = PlayerForm()
        formset = BeybladeFormSetCreate()

    return render(request, 'player_beyblade_form.html', {
        'title': 'プレイヤー・ベイブレード作成',
        'player_form': player_form,
        'formset': formset
    })

@login_required
def player_beyblade_update(request, pk):
    player = get_object_or_404(Player, pk=pk, user=request.user,)

    if request.method == 'POST':
        player_form = PlayerForm(request.POST, instance=player)
        formset = BeybladeFormSetUpdate(request.POST, instance=player)

        if player_form.is_valid() and formset.is_valid():
            player_form.save()
            formset.save()
            return redirect('player_list')
    else:
        player_form = PlayerForm(instance=player)
        formset = BeybladeFormSetUpdate(instance=player)

    return render(request, 'player_beyblade_form.html', {
        'title': 'プレイヤー・ベイブレード編集',
        'player_form': player_form,
        'formset': formset
    })

def player_beyblade_delete(request, pk):
    # ベイブレードを取得
    beyblade = get_object_or_404(Beyblade, pk=pk, user=request.user)

    if request.method == 'POST':
        # ベイブレードを削除
        beyblade.delete()
        return redirect('player_list')  # 削除後、プレイヤー一覧にリダイレクト

    return render(request, 'beyblade_confirm_delete.html', {'beyblade': beyblade})

def match_create(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('match_list')  # 試合作成後は試合一覧にリダイレクト
    else:
        form = MatchForm()  # 空のフォームを表示

    return render(request, 'match_form.html', {'form': form})

def match_update(request, pk):
    match = get_object_or_404(Match, pk=pk, user=request.user)

    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('match_list')  # 試合更新後は試合一覧にリダイレクト
    else:
        form = MatchForm(instance=match)

    return render(request, 'match_form.html', {'form': form})

def match_delete(request, pk):
    match = get_object_or_404(Match, pk=pk, user=request.user)

    if request.method == 'POST':
        match.delete()  # 試合を削除
        return redirect('match_list')  # 削除後に試合一覧にリダイレクト

    return render(request, 'match_confirm_delete.html', {'match': match})

def match_list(request):
    matches = Match.objects.all().order_by('-date')  # 試合を日付の降順で取得
    return render(request, 'match_list.html', {'matches': matches})

class PlayerUpdateView(UpdateView):
    model = Player
    fields = ['name']
    template_name = 'player_update.html'
    success_url = reverse_lazy('player_list')