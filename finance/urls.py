
from finance.dashboard import dashboard

#Money Supply
from finance.dashboard.money_supply import money_supply
from finance.dashboard.money_supply import domestic_credit
from finance.dashboard.money_supply import gold_forex_holding
from finance.dashboard.money_supply import reserve_money

#Loan Disbursement
from finance.dashboard.financial_intermediation.banks import loan_disbursement_banks
from finance.dashboard.financial_intermediation.banks import loan_disbursement_client
from finance.dashboard.financial_intermediation.banks import loan_disbursement_sector

#Loan Collection
from finance.dashboard.financial_intermediation.banks import loan_collection_banks
from finance.dashboard.financial_intermediation.banks import loan_collection_client
from finance.dashboard.financial_intermediation.banks import loan_collection_sector

#Loan Outstanding
from finance.dashboard.financial_intermediation.banks import loan_outstanding_banks
from finance.dashboard.financial_intermediation.banks import loan_outstanding_client
from finance.dashboard.financial_intermediation.banks import loan_outstanding_sector
															 
			  
	
from django.urls import path
from . import views

urlpatterns =[

    path('', views.dashboard, name='dashboard'),  

   #Money Supply
    path('money_supply', views.money_supply, name='money_supply'),   
    path('domestic_credit', views.domestic_credit, name='domestic_credit'),   
    path('gold_forex_holding', views.gold_forex_holding, name='gold_forex_holding'),   
    path('reserve_money', views.reserve_money, name='reserve_money'),   

    #Loan Disbursement
    path('loan_disbursement_banks', views.loan_disbursement_banks, name='loan_disbursement_banks'),   
    path('loan_disbursement_client', views.loan_disbursement_client, name='loan_disbursement_client'),   
    path('loan_disbursement_sector', views.loan_disbursement_sector, name='loan_disbursement_sector'),   

    #Loan Collection
    path('loan_collection_banks', views.loan_collection_banks, name='loan_collection_banks'),   
    path('loan_collection_client', views.loan_collection_client, name='loan_collection_client'),   
    path('loan_collection_sector', views.loan_collection_sector, name='loan_collection_sector'),   

	#Loan Outstanding
    path('loan_outstanding_banks', views.loan_outstanding_banks, name='loan_outstanding_banks'),
    path('loan_outstanding_client', views.loan_outstanding_client, name='loan_outstanding_client'),  
    path('loan_outstanding_sector', views.loan_outstanding_sector, name='loan_outstanding_sector'),
]