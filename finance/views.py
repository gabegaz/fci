from django.shortcuts import render


def dashboard(request):
    return render(request, 'finance/dashboard.html')


def money_supply(request):
    return render(request, 'finance/money_supply/money_supply.html')


def domestic_credit(request):
    return render(request, 'finance/money_supply/domestic_credit.html')


def forex_holding(request):
    return render(request, 'finance/money_supply/forex_holding.html')