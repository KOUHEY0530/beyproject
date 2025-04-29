from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, PlayerForm, BeybladeForm
from .models import Match
from .forms import MatchForm

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
            form.save()
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
    matches = Match.objects.select_related('player1', 'player2', 'winner').order_by('-date')
    return render(request, 'match_list.html', {'matches': matches})

@login_required
def match_create(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('match_list')  # 登録後は勝敗一覧へ
    else:
        form = MatchForm()
    return render(request, 'match_form.html', {'form': form})
