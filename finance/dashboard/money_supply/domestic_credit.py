# -*- coding: utf-8 -*-


import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
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

app = DjangoDash('DomesticCredit', add_bootstrap_links=True, 
  suppress_callback_exceptions=True, 
  external_stylesheets=[dbc.themes.BOOTSTRAP])


data = 'D:/projects/World_Bank_FCI/data/money_supply/'

df_level   =  pd.read_excel(data+'domestic_credit.xlsx',
                sheet_name='domestic_credit_level',
                skiprows=1, nrows=41, usecols='A:I')


df_share   =  pd.read_excel(data+'domestic_credit.xlsx',
                sheet_name='domestic_credit_share',
                skiprows=1, nrows=41, usecols='A:I')


df_growth   =  pd.read_excel(data+'domestic_credit.xlsx',
                sheet_name='domestic_credit_growth',
                skiprows=1, nrows=41, usecols='A:I')


df_contrib  =  pd.read_excel(data+'domestic_credit.xlsx',
                sheet_name='domestic_credit_contrib',
                skiprows=1, nrows=41, usecols='A:I')


cols = [i for i in df_level.columns]


df_level = pd.melt(df_level, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Domestic Credit', value_name='level')

df_share = pd.melt(df_share, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Domestic Credit', value_name='share')

df_growth = pd.melt(df_growth, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Domestic Credit', value_name='growth')

df_contrib = pd.melt(df_contrib, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Domestic Credit', value_name='contrib')

categories = df_level['Domestic Credit'].unique()


height = 600
width  = 700



dropdown = dbc.Card([
     dcc.Dropdown(
        id='id_aggregates',
        options=[{'label': i, 'value': i} for i in categories],
        multi = True,
        value=['Domestic Credit-Total']),
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
    [Input(component_id='id_aggregates', component_property='value')]
    )
def level(aggregates):
    dff_level = df_level[df_level['Domestic Credit'].isin(aggregates)]
    fig = px.area(dff_level, x= 'year',
                  y = 'level',
                  color='Domestic Credit',
                  title = "DC #1: Domestic Credit (Billions of Birr)",
                  labels={
                     "year": "Time in year",
                     "level": "Value (Millions of Birr)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig
     
     
@app.callback(
    Output(component_id='id_share', component_property='figure'),
    [Input(component_id='id_aggregates', component_property='value')]
    )
def share(aggregates):
    dff_share = df_share.loc[df_share['Domestic Credit'] != 'Domestic Credit-Total']
    dff_share = df_share[df_share['Domestic Credit'].isin(aggregates)]
    fig = px.line(dff_share, x= 'year',
                  y = 'share',
                  color='Domestic Credit',
                  title = "DC #2: Share in Domestic Credit (Percent)",
                  labels={
                     "year": "Time in year",
                     "share": "Share (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig


@app.callback(
    Output(component_id='id_growth', component_property='figure'),
    [Input(component_id='id_aggregates', component_property='value')]
    )
def growth(aggregates):
    dff_growth = df_growth[df_growth['Domestic Credit'].isin(aggregates)]
    fig = px.line(dff_growth, x= 'year',
                  y = 'growth',
                  color='Domestic Credit',
                  title = "DC #3: Growth Rate of Domestic Credit (Percent)", 
                  labels={
                     "year": "Time in year",
                     "growth": "Growth rate (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig


@app.callback(
    Output(component_id='id_contrib', component_property='figure'),
    [Input(component_id='id_aggregates', component_property='value')]
    )
def contribution(aggregates):
    dff_contrib = df_contrib[df_contrib['Domestic Credit'].isin(aggregates)]
    fig = px.line(dff_contrib, x= 'year',
                  y = 'contrib',
                  color='Domestic Credit',
                  title = "DC #4: Contribution to Growth of Domestic Credit (Percent)", 
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