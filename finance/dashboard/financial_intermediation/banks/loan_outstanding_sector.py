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

app = DjangoDash('LoanOutstandingSector', add_bootstrap_links=True, 
  suppress_callback_exceptions=True, 
  external_stylesheets=[dbc.themes.BOOTSTRAP])


data = 'D:/projects/World_Bank_FCI/data/financial_intermediation/banks/'

df_level   =  pd.read_excel(data+'loan_outstanding_sector.xlsx',
                sheet_name='loan_outstanding_sector_level',
                skiprows=1, nrows=39, usecols='A:N')

df_share   =  pd.read_excel(data+'loan_outstanding_sector.xlsx',
                sheet_name='loan_outstanding_sector_share',
                skiprows=1, nrows=39, usecols='A:N')


df_growth   =  pd.read_excel(data+'loan_outstanding_sector.xlsx',
                sheet_name='loan_outstanding_sector_growth',
                skiprows=1, nrows=39, usecols='A:N')


df_contrib  =  pd.read_excel(data+'loan_outstanding_sector.xlsx',
                sheet_name='loan_outstanding_sector_contrib',
                skiprows=1, nrows=39, usecols='A:N')


cols = [i for i in df_level.columns]


df_level = pd.melt(df_level, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Sector', value_name='level')

df_share = pd.melt(df_share, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Sector', value_name='share')

df_growth = pd.melt(df_growth, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Sector', value_name='growth')

df_contrib = pd.melt(df_contrib, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Sector', value_name='contrib')

categories = df_level['Sector'].unique()


height = 700
width  = 700




dropdown = dbc.Card([
     dcc.Dropdown(
        id='id_sector',
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
    [Input(component_id='id_sector', component_property='value')]
    )
def level(sector):
    dff_level = df_level[df_level['Sector'].isin(sector)]
    fig = px.line(dff_level, x= 'year',
                  y = 'level',
                  color='Sector',
                  title = "LO #9: Loan Outstanding (Millions of Birr)-Sector",
                  labels={
                     "year": "Time in year",
                     "level": "Value (Millions of Birr)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig
     
@app.callback(
    Output(component_id='id_share', component_property='figure'),
    [Input(component_id='id_sector', component_property='value')]
    )
def share(sector):
    dff_share = df_share.loc[df_share['Sector'] != 'All Sectors']
    dff_share = dff_share[dff_share['Sector'].isin(sector)]
    fig = px.line(dff_share, x= 'year',
                  y = 'share',
                  color='Sector',
                  title = "LO #10: Share of Loan Outstanding (Percent)-Sector",
                  labels={
                     "year": "Time in year",
                     "share": "Share (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig


@app.callback(
    Output(component_id='id_growth', component_property='figure'),
    [Input(component_id='id_sector', component_property='value')]
    )
def growth(sector):
    dff_growth = df_growth[df_growth['Sector'].isin(sector)]
    fig = px.line(dff_growth, x= 'year',
                  y = 'growth',
                  color='Sector',
                  title = "LO #11: Growth Rate of Loan Outstanding (Percent)-Sector",
                  labels={
                     "year": "Time in year",
                     "growth": "Growth rate (percent)",
                     }
                 ).for_each_trace(lambda t: t.update(name=t.name.split("=")[0]))
    return fig


@app.callback(
    Output(component_id='id_contrib', component_property='figure'),
    [Input(component_id='id_sector', component_property='value')]
    )
def contribution(sector):
    dff_contrib = df_contrib[df_contrib['Sector'].isin(sector)]
    fig = px.line(dff_contrib, x= 'year',
                  y = 'contrib',
                  color='Sector',
                  title = "LO #12: Contribution to Growth of Loan Outstanding (Percent)-Sector",
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