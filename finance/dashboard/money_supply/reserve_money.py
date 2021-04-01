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

app = DjangoDash('ReserveMoney', add_bootstrap_links=True, 
  suppress_callback_exceptions=True, 
  external_stylesheets=[dbc.themes.BOOTSTRAP])


# Data from http://ghdx.healthdata.org/gbd-results-tool
data = 'D:/projects/World_Bank_FCI/data/money_supply/'

df_level   =  pd.read_excel(data+'reserve_money.xlsx',
                sheet_name='reserve_money_level',
                skiprows=1, nrows=11, usecols='A:G')

df_growth   =  pd.read_excel(data+'reserve_money.xlsx',
                sheet_name='reserve_money_growth',
                skiprows=1, nrows=11, usecols='A:G')



cols = [i for i in df_level.columns]


df_level = pd.melt(df_level, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Reserves', value_name='level')

df_growth = pd.melt(df_growth, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Reserves', value_name='growth')

categories = df_level['Reserves'].unique()


height = 600
width  = 700


dropdown = dbc.Card([
     dcc.Dropdown(
        id='id_reserves',
        options=[{'label': i, 'value': i} for i in categories],
        multi = True,
        value=['Reserve Money']),
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
      


app.layout = html.Div([
  html.Br(),
  html.Br(),
  dbc.Row([
        dbc.Col(dropdown, md=12),
        dbc.Col(level, lg=6),
        dbc.Col(growth, lg=6),

  ]),
 
])


@app.callback(
    Output(component_id='id_level', component_property='figure'),
    [Input(component_id='id_reserves', component_property='value')]
    )
def level(reserves):
    dff_level = df_level[df_level['Reserves'].isin(reserves)]
    fig = px.area(dff_level, x= 'year',
                  y = 'level',
                  color='Reserves',
                  title = "RM #1: Reserve Money (Millions of Birr)",
                  labels={
                     "year": "Time in year",
                     "level": "Value (Millions of Birr)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig
     

@app.callback(
    Output(component_id='id_growth', component_property='figure'),
    [Input(component_id='id_reserves', component_property='value')]
    )
def growth(reserves):
    dff_growth = df_growth[df_growth['Reserves'].isin(reserves)]
    fig = px.line(dff_growth, x= 'year',
                  y = 'growth',
                  color='Reserves',
                  title = "RM #2: Growth Rate of Reserve Money (Percent)", 
                  labels={
                     "year": "Time in year",
                     "growth": "Growth rate (percent)",
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