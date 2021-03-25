
from finance.dashboard import dashboard
from finance.dashboard.monetary import money_supply
from finance.dashboard.monetary import domestic_credit
from finance.dashboard.monetary import forex_holding



from django.urls import path
from . import views

urlpatterns =[

    path('', views.dashboard, name='dashboard'),   
    path('money_supply', views.money_supply, name='money_supply'),   
    path('domestic_credit', views.domestic_credit, name='domestic_credit'),   
    path('forex_holding', views.forex_holding, name='forex_holding'),   

]