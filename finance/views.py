from django.shortcuts import render


def dashboard(request):
    return render(request, 'finance/dashboard.html')


#Money Supply
def money_supply(request):
    return render(request, 'finance/money_supply/money_supply.html')

def domestic_credit(request):
    return render(request, 'finance/money_supply/domestic_credit.html')

def gold_forex_holding(request):
    return render(request, 'finance/money_supply/gold_forex_holding.html')

def reserve_money(request):
    return render(request, 'finance/money_supply/reserve_money.html')


#Loan Disbursement
def loan_disbursement_client(request):
    return render(request, 'finance/financial_intermediation/banks/loan_disbursement_client.html')
  
def loan_disbursement_sector(request):
    return render(request, 'finance/financial_intermediation/banks/loan_disbursement_sector.html')

def loan_disbursement_banks(request):
    return render(request, 'finance/financial_intermediation/banks/loan_disbursement_banks.html')


#Loan Collection
def loan_collection_banks(request):
    return render(request, 'finance/financial_intermediation/banks/loan_collection_banks.html')

def loan_collection_client(request):
    return render(request, 'finance/financial_intermediation/banks/loan_collection_client.html')

def loan_collection_sector(request):
    return render(request, 'finance/financial_intermediation/banks/loan_collection_sector.html')


#Loan Outstanding
def loan_outstanding_banks(request):
    return render(request, 'finance/financial_intermediation/banks/loan_outstanding_banks.html')

def loan_outstanding_client(request):
    return render(request, 'finance/financial_intermediation/banks/loan_outstanding_client.html')

def loan_outstanding_sector(request):
 	return render(request, 'finance/financial_intermediation/banks/loan_outstanding_sector.html')
