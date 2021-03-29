# -*- coding: utf-8 -*-

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

app = DjangoDash('GoldForexHolding', add_bootstrap_links=True, 
  suppress_callback_exceptions=True, 
  external_stylesheets=[dbc.themes.BOOTSTRAP])

data = 'D:/projects/World_Bank_FCI/data/money_supply/'
df   =  pd.read_excel(data+'gold_forex_holding.xlsx',
        sheet_name='gold_forex_holding_long')

categories = df['Forex holding'].unique()


dropdown = dbc.Card([
     dcc.Dropdown(
        id='id_holding',
        options=[{'label': i, 'value': i} for i in categories],
        multi = True,
        value=categories),
  ],body=True)
   

levels =dbc.Card([
     dcc.Graph(id = 'id_levels'),
     html.Small("Source: National Bank of Ethiopia"),       
     dbc.CardHeader(
            dbc.Button(
                "Notes",
                color="link",
                id="button_levels")
            ),
    
    dbc.Collapse(
        dbc.CardBody("""

                     This variable is stock. So, one would expect an increasing trend over time.
                     
                     """),
        id="collapse_levels", is_open=False
    ),
        
    ],
    body=True,
 )
       
growth =dbc.Card([
        dcc.Graph(id = 'id_growth'),
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
      
share =dbc.Card([
        dcc.Graph(id = 'id_share'),
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
  



contribution =dbc.Card([
        dcc.Graph(id = 'id_contribution'),
        html.Small("Source: National Bank of Ethiopia"),       
        dbc.CardHeader(
            dbc.Button(
                "Notes",
                color="link",
                id="button_contribution",
            )
    ),
    
    dbc.Collapse(
        dbc.CardBody("""
                     Shares for currency outside banks and demand deposits were computed from money supply; while
                     shares for money supply and quasi money were computed from broad money 
                     
                     """),
        id="collapse_contribution", is_open=False
    ),
     
    ], 
  body=True,
 )
  




 
app.layout = html.Div([
  html.Br(),
  html.Br(),
  dbc.Row([
        dbc.Col(dropdown, md=12),
        dbc.Col(levels, lg=6),
        dbc.Col(growth, lg=6),
        dbc.Col(share, lg=6),
        dbc.Col(contribution, lg=6),

  ]),
 
])


@app.callback(
    Output(component_id='id_levels', component_property='figure'),
    [Input(component_id='id_holding', component_property='value')]
    )
def levels(forex_holding):
    dff = df[df['Forex holding'].isin(forex_holding)]
    fig = px.line(dff, x= 'year',
                  y = 'levels',
                  color='Forex holding',
                  title = "GF #1: Net Forex Holding for the Year Ending July (Billions of Birr)",
                  labels={
                     "year": "Time in year",
                     "levels": "Value (Billions of Birr)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig
     

@app.callback(
    Output(component_id='id_growth', component_property='figure'),
    [Input(component_id='id_holding', component_property='value')]
    )
def growth(forex_holding):
    
    dff = df[df['Forex holding'].isin(forex_holding)]
    fig = px.line(dff, x= 'year',
                  y = 'growth',
                  color='Forex holding',
                  title = "GF #2: Growth Rates in Net Forex Holding for the Year Ending July (Percent)",
                  labels={
                     "year": "Time in year",
                     "growth": "Growth rate (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig


@app.callback(
    Output(component_id='id_share', component_property='figure'),
    [Input(component_id='id_holding', component_property='value')]
    )
def share(forex_holding):
    dff = df[df['Forex holding'].isin(forex_holding)]
    fig = px.line(dff, x= 'year',
                  y = 'share',
                  color='Forex holding',
                  title = "GF #3: Share of Net Forex Holding for the Year Ending July (Percent)",
                  labels={
                     "year": "Time in year",
                     "share": "Share (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig



@app.callback(
    Output(component_id='id_contribution', component_property='figure'),
    [Input(component_id='id_holding', component_property='value')]
    )
def share(forex_holding):
    dff = df[df['Forex holding'].isin(forex_holding)]
    fig = px.line(dff, x= 'year',
                  y = 'contribution',
                  color='Forex holding',
                  title = "GF #4: Contribution to Growth of Net Forex Holding for the Year Ending July (Percent)",
                  labels={
                     "year": "Time in year",
                     "contribution": "Contribution (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig



#Notes callbacks for levels
@app.callback(
    Output("collapse_levels", "is_open"),
    [Input("button_levels", "n_clicks")],
    [State("collapse_levels", "is_open")],
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
    Output("collapse_contribution", "is_open"),
    [Input("button_contribution", "n_clicks")],
    [State("collapse_contribution", "is_open")],
)
def note3(n, is_open):
    if n:
        return not is_open
    return is_open