from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    """Главная страница"""
    return render(request, 'core/index.html')


@login_required
def profile(request):
    """Личный кабинет пользователя"""
    return render(request, 'accounts/profile.html')


@login_required
def order_detail(request, order_id):
    """Детализация заказа в личном кабинете"""
    return render(request, 'accounts/order_detail.html')