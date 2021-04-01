# -*- coding: utf-8 -*-

import pandas as pd    
import plotly          
import plotly.io as pio
import plotly.graph_objects as go

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

app = DjangoDash('LoanDisbursementBanks', add_bootstrap_links=True, 
  suppress_callback_exceptions=True, 
  external_stylesheets=[dbc.themes.BOOTSTRAP])


data = 'D:/projects/World_Bank_FCI/data/financial_intermediation/banks/'

df_level   =  pd.read_excel(data+'loan_disbursement_banks.xlsx',
                sheet_name='loan_disbursement_banks_level',
                skiprows=1, nrows=40, usecols='A:W')

df_share   =  pd.read_excel(data+'loan_disbursement_banks.xlsx',
                sheet_name='loan_disbursement_banks_share',
                skiprows=1, nrows=40, usecols='A:W')


df_growth   =  pd.read_excel(data+'loan_disbursement_banks.xlsx',
                sheet_name='loan_disbursement_banks_growth',
                skiprows=1, nrows=40, usecols='A:W')


df_contrib  =  pd.read_excel(data+'loan_disbursement_banks.xlsx',
                sheet_name='loan_disbursement_banks_contrib',
                skiprows=1, nrows=40, usecols='A:W')


cols = [i for i in df_level.columns]


df_level = pd.melt(df_level, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Lender', value_name='level')

df_share = pd.melt(df_share, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Lender', value_name='share')

df_growth = pd.melt(df_growth, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Lender', value_name='growth')

df_contrib = pd.melt(df_contrib, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Lender', value_name='contrib')

categories = df_level['Lender'].unique()


height = 700
width  = 700



dropdown = dbc.Card([
     dcc.Dropdown(
        id='id_lender',
        options=[{'label': i, 'value': i} for i in categories],
        multi = True,
        value=categories),
  ],body=True)
   

level =dbc.Card([
     dcc.Graph(
      id = 'id_level', 
      config={'displaylogo': False},
      style={'height': height, 'width': width}
      ),

     html.Small("Source: National Bank of Ethiopia"),       
     dbc.CardHeader(
            dbc.Button(
                "Notes",
                color="link",
                id="button_level")
            ),
    
    dbc.Collapse(
        dbc.CardBody("""

                     This variable is stock. So, one would expect an increasing trend over time.
                     
                     """),
        id="collapse_level", is_open=False
    ),
        
    ],
    body=True,
 )
     
share =dbc.Card([
    dcc.Graph(
      id = 'id_share', 
      config={'displaylogo': False},
      style={'height': height, 'width':width}
      ),

      html.Small("Source: National Bank of Ethiopia"),       
        dbc.CardHeader(
            dbc.Button(
                "Notes",
                color="link",
                id="button_share",
            )
    ),
    
    dbc.Collapse(
        dbc.CardBody("""
                     Shares for currency outside banks and demand deposits were computed from money supply; while
                     shares for money supply and quasi money were computed from broad money 
                     
                     """),
        id="collapse_share", is_open=False
    ),
     
    ], 
  body=True,
 )
  

growth =dbc.Card([
        dcc.Graph(
        id = 'id_growth', 
        config={'displaylogo': False},
        style={'height': height, 'width':width}
      ),

        html.Small("Source: National Bank of Ethiopia"),       
        dbc.CardHeader(
            dbc.Button(
                "Notes",
                color="link",
                id="button_growth",
            )
    ),
    
    dbc.Collapse(
        dbc.CardBody("""
                     Growth rate (in percent)
                         
                     """),
        id="collapse_growth", is_open=False
    ),
     
    ],
    body=True,
  )
      

contrib =dbc.Card([
      dcc.Graph(
        id = 'id_contrib', 
        config={'displaylogo': False},
        style={'height': height, 'width':width}
      ),

        html.Small("Source: National Bank of Ethiopia"),       
        dbc.CardHeader(
            dbc.Button(
                "Notes",
                color="link",
                id="button_contrib",
            )
    ),
    
    dbc.Collapse(
        dbc.CardBody("""
                     Shares for currency outside banks and demand deposits were computed from money supply; while
                     shares for money supply and quasi money were computed from broad money 
                     
                     """),
        id="collapse_contrib", is_open=False
    ),
     
    ], 
  body=True,
 )
 

app.layout = html.Div([
  html.Br(),
  html.Br(),
  dbc.Row([
        dbc.Col(dropdown, md=12),
        dbc.Col(level, lg=6),
        dbc.Col(share, lg=6),
        dbc.Col(growth, lg=6),
        dbc.Col(contrib, lg=6),

 ]),
 
])


@app.callback(
    Output(component_id='id_level', component_property='figure'),
    [Input(component_id='id_lender', component_property='value')]
    )
def level(lender):
    dff_level = df_level[df_level['Lender'].isin(lender)]
    fig = px.line(dff_level, x= 'year',
                  y = 'level',
                  color='Lender',
                  title = "LD #1: Loan Disbursements (Millions of Birr)-Lender",
                  labels={
                     "year": "Time in year",
                     "level": "Value (Millions of Birr)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig
     
@app.callback(
    Output(component_id='id_share', component_property='figure'),
    [Input(component_id='id_lender', component_property='value')]
    )

def share(lender):
    dff_share = df_share.loc[df_share['Lender']!='All Banks']
    dff_share = dff_share[dff_share['Lender'].isin(lender)]
    fig = px.line(dff_share, x= 'year',
                  y = 'share',
                  color='Lender',
                  title = "LD #2: Share of Loan Disbursements(Percent)-Lender",
                  labels={
                     "year": "Time in year",
                     "share": "Share (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig


@app.callback(
    Output(component_id='id_growth', component_property='figure'),
    [Input(component_id='id_lender', component_property='value')]
    )
def growth(lender):
    dff_growth = df_growth[df_growth['Lender'].isin(lender)]
    fig = px.line(dff_growth, x= 'year',
                  y = 'growth',
                  color='Lender',
                  title = "LD #3: Growth Rate of Loan Disbursements(Percent)-Lender", 
                  labels={
                     "year": "Time in year",
                     "growth": "Growth rate (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig


@app.callback(
    Output(component_id='id_contrib', component_property='figure'),
    [Input(component_id='id_lender', component_property='value')]
    )
def contribution(lender):
    dff_contrib = df_contrib[df_contrib['Lender'].isin(lender)]
    fig = px.line(dff_contrib, x= 'year',
                  y = 'contrib',
                  color='Lender',
                  title = "LD #4: Contribution to Growth of Loan Disbursements(Percent)-Lender", 
                  labels={
                     "year": "Time in year",
                     "contrib": "Contribution (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig



#Notes callbacks for levels
@app.callback(
    Output("collapse_level", "is_open"),
    [Input("button_level", "n_clicks")],
    [State("collapse_level", "is_open")],
)
def note3(n, is_open):
    if n:
        return not is_open
    return is_open


#Notes callbacks for growth
@app.callback(
    Output("collapse_growth", "is_open"),
    [Input("button_growth", "n_clicks")],
    [State("collapse_growth", "is_open")],
)
def note3(n, is_open):
    if n:
        return not is_open
    return is_open


#Notes callbacks for share
@app.callback(
    Output("collapse_share", "is_open"),
    [Input("button_share", "n_clicks")],
    [State("collapse_share", "is_open")],
)
def note3(n, is_open):
    if n:
        return not is_open
    return is_open


#Notes callbacks for contribution
@app.callback(
    Output("collapse_contrib", "is_open"),
    [Input("button_contrib", "n_clicks")],
    [State("collapse_contrib", "is_open")],
)
def note3(n, is_open):
    if n:
        return not is_open
    return is_open