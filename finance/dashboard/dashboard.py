# -*- coding: utf-8 -*-

import pandas as pd   
import plotly           
import plotly.io as pio
import plotly.graph_objects as go

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

app = DjangoDash('DashBoard', add_bootstrap_links=True, 
  suppress_callback_exceptions=True, 
  external_stylesheets=[dbc.themes.BOOTSTRAP])


money_supply = 'D:/projects/World_Bank_FCI/data/money_supply/'
fin_inter    = 'D:/projects/World_Bank_FCI/data/financial_intermediation/banks/'

ms_level   =  pd.read_excel(money_supply+'money_supply.xlsx',
                sheet_name='money_supply_level',
                skiprows=1, nrows=40, usecols='A:F')

ms_share   =  pd.read_excel(money_supply+'money_supply.xlsx',
                sheet_name='money_supply_share',
                skiprows=1, nrows=40, usecols='A:F')

ms_growth   =  pd.read_excel(money_supply+'money_supply.xlsx',
                sheet_name='money_supply_growth',
                skiprows=1, nrows=40, usecols='A:F')


dc_level   =  pd.read_excel(money_supply+'domestic_credit.xlsx',
                sheet_name='domestic_credit_level',
                skiprows=1, nrows=41, usecols='A:I')

dc_share   =  pd.read_excel(money_supply+'domestic_credit.xlsx',
                sheet_name='domestic_credit_share',
                skiprows=1, nrows=41, usecols='A:I')

dc_growth   =  pd.read_excel(money_supply+'domestic_credit.xlsx',
                sheet_name='domestic_credit_growth',
                skiprows=1, nrows=41, usecols='A:I')

dc_level = dc_level[['year', 'Domestic Credit-Total']]
dc_share = dc_share[['year', 'Domestic Credit-Total']]
dc_growth = dc_growth[['year', 'Domestic Credit-Total']]

df_level  = ms_level.merge(dc_level, how='inner', on='year')
df_share  = ms_share.merge(dc_share, how='inner', on='year')
df_growth = ms_growth.merge(dc_growth, how='inner', on='year')

cols = [i for i in df_level.columns]


df_level = pd.melt(df_level, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Monetary Aggregates', value_name='level_alues')

df_share = pd.melt(df_share, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Monetary Aggregates', value_name='share_alues')

df_growth = pd.melt(df_growth, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Monetary Aggregates', value_name='growth_values')


categories = df_level['Monetary Aggregates'].unique()

height = 600
width  = 600

dropdown_level = dbc.Card([
	 dbc.CardHeader("Levels (Billions of Birr)"),
     dcc.Dropdown(
        id='dropdown_level',
        options=[{'label': i, 'value': i} for i in categories],
        multi = True,
        value=['Money supply']),
  ],body=True)
   

dropdown_share = dbc.Card([
	 dbc.CardHeader("Shares (Percent)"),
     dcc.Dropdown(
        id='dropdown_share',
        options=[{'label': i, 'value': i} for i in categories],
        multi = True,
        value=['Money supply']),
  ],body=True)
   

dropdown_growth = dbc.Card([
	 dbc.CardHeader("Growth rates (Percent)"),

     dcc.Dropdown(
        id='dropdown_growth',
        options=[{'label': i, 'value': i} for i in categories],
        multi = True,
        value=['Money supply']),
  ],body=True)
   



level =dbc.Card([
     dcc.Graph(
      id = 'id_level', 
      config={'displaylogo': False},
      # style={'height': height, 'width': width}
      ),

     html.Small("Source: National Bank of Ethiopia"),       
     
  ],
    body=True,
 )
    
app.layout = html.Div([
  html.Br(),
  html.Br(),
  dbc.Row([
        dbc.Col(dropdown_level, lg=4),
        dbc.Col(dropdown_share, lg=4),
        dbc.Col(dropdown_growth, lg=4),
        dbc.Col(level, lg=12),
 ]),
 
])



@app.callback(
    Output(component_id='id_level', component_property='figure'),
    [Input(component_id='dropdown_level', component_property='value'),
     Input(component_id='dropdown_share', component_property='value'),
     Input(component_id='dropdown_growth', component_property='value')
    ])
def level(level, share, growth):

    if len(level) > 0:
    	dff_level = df_level[df_level['Monetary Aggregates'].isin(level)]
    	fig = px.area(dff_level, x= 'year',
    		y = 'Values',
    		color = 'Monetary Aggregates',
    		title = "Figure #0: Monetary Aggregates",
    		labels={
    		"year": "Time in year",
    		"Values": "Value (Billions of Birr)",
    		}
    		).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    	return fig

    elif len(share) > 0:
    	dff_share = df_share[df_share['Monetary Aggregates'].isin(share)]
    	fig = px.line(dff_share, x= 'year',
    		y = 'Values',
    		color = 'Monetary Aggregates',
    		title = "Figure #0: MAMonetary Aggregates",
    		labels={
                     "year": "Time in year",
                     "Values": "Share (Percent)",
                     }
                     ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    	return fig
     
    else:
    	dff_growth = df_growth[df_growth['Monetary Aggregates'].isin(growth)]
    	fig = px.line(dff_growth, x= 'year',
    		y = 'Values',
    		color = 'Monetary Aggregates',
    		title = "Figure #0: Monetary Aggregates",
    		labels={
                     "year": "Time in year",
                     "Values": "Growth Rate (Percent)",
                     }
                     ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    	return fig