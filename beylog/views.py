from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, PlayerForm, BeybladeForm
from .models import Match
from .forms import MatchForm
from .forms import PlayerBeybladeForm, Beyblade, Player
from django.shortcuts import get_object_or_404
from .forms import BeybladeFormSet
from django.db.models import Count, Q

@login_required
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 登録後はログイン画面へ
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def player_create(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            return redirect('player_list')
    else:
        form = PlayerForm()
    return render(request, 'player_form.html', {'form': form})

@login_required
def beyblade_create(request):
    if request.method == 'POST':
        form = BeybladeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('beyblade_list')
    else:
        form = BeybladeForm()
    return render(request, 'beyblade_form.html', {'form': form})

@login_required
def match_list(request):
    matches = Match.objects.all().order_by('-date')
    return render(request, 'match_list.html', {'matches': matches})

def player_list(request): #プレイヤー一覧表示
    players = Player.objects.filter(user=request.user)
    return render(request, 'player_list.html', {'players': players})

@login_required
def match_create(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('match_list')  # 登録後は勝敗一覧へ
        else:
            print(form.errors)  # コンソールにも出す
    else:
        form = MatchForm()
    return render(request, 'match_form.html', {'form': form})

@login_required
def match_update(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('match_list')
    else:
        form = MatchForm(instance=match)
    return render(request, 'match_form.html', {'form': form})

@login_required
def match_delete(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        match.delete()
        return redirect('match_list')
    return render(request, 'match_confirm_delete.html', {'match': match})

@login_required
# 追加
def player_beyblade_create(request):
    if request.method == 'POST':
        player_form = PlayerForm(request.POST)

        if player_form.is_valid():
            player = player_form.save(commit=False)
            player.user = request.user
            player.save()

            formset = BeybladeFormSet(request.POST, instance=player)  # ←ここ重要
            if formset.is_valid():
                formset.save()
                return redirect('player_list')
        else:
            formset = BeybladeFormSet(request.POST)  # プレイヤー保存失敗時
    else:
        player_form = PlayerForm()
        formset = BeybladeFormSet()

    return render(request, 'player_beyblade_form.html', {
        'player_form': player_form,
        'formset': formset,
    })

@login_required
# 編集
def player_beyblade_update(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    try:
        beyblade = player.beyblades.first()  # そのプレイヤーのベイブレード1つ取得
    except Beyblade.DoesNotExist:
        beyblade = None

    if request.method == 'POST':
        form = PlayerBeybladeForm(request.POST, request.FILES)
        if form.is_valid():
            player.name = form.cleaned_data['player_name']
            player.save()
            if beyblade:
                beyblade.name = form.cleaned_data['beyblade_name']
            return redirect('player_list')
    else:
        form = PlayerBeybladeForm(initial={
            'player_name': player.name,
            'beyblade_name': beyblade.name if beyblade else '',
        })

    return render(request, 'player_beyblade_form.html', {'form': form, 'update': True})

@login_required
# 削除
def player_beyblade_delete(request, player_id):
    player = get_object_or_404(Player, id=player_id)

    if request.method == 'POST':
        player.delete()  # プレイヤーと紐づくベイも一緒に削除
        return redirect('player_list')

    return render(request, 'player_beyblade_confirm_delete.html', {'player': player})

@login_required
# プレイヤー・ベイブレード編集
def player_beyblade_update(request, player_id):
    player = get_object_or_404(Player, id=player_id)

    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        formset = BeybladeFormSet(request.POST, request.FILES, instance=player)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('player_list')
    else:
        form = PlayerForm(instance=player)
        formset = BeybladeFormSet(instance=player)

    return render(request, 'player_beyblade_form.html', {
        'form': form,
        'formset': formset,
        'title': 'プレイヤー＋ベイブレード編集'
    })

@login_required
def player_beyblade_delete(request, player_id):
    player = get_object_or_404(Player, id=player_id)

    if request.method == 'POST':
        player.delete()
        return redirect('player_list')

    return render(request, 'player_beyblade_confirm_delete.html', {'player': player})

@login_required
def player_stats(request):
    players = Player.objects.all()

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