# Environment used: dash1_8_0_env
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

app = DjangoDash('MoneySupply', add_bootstrap_links=True, 
  suppress_callback_exceptions=True, 
  external_stylesheets=[dbc.themes.BOOTSTRAP])


# Data from http://ghdx.healthdata.org/gbd-results-tool
data = 'D:/projects/World_Bank_FCI/data/money_supply/'

df_level   =  pd.read_excel(data+'money_supply.xlsx',
                sheet_name='money_supply_level',
                skiprows=1, nrows=40, usecols='A:F')



df_share   =  pd.read_excel(data+'money_supply.xlsx',
                sheet_name='money_supply_share',
                skiprows=1, nrows=40, usecols='A:W')


df_growth   =  pd.read_excel(data+'money_supply.xlsx',
                sheet_name='money_supply_growth',
                skiprows=1, nrows=40, usecols='A:W')


df_contrib  =  pd.read_excel(data+'money_supply.xlsx',
                sheet_name='money_supply_contrib',
                skiprows=1, nrows=40, usecols='A:W')


cols = [i for i in df_level.columns]


df_level = pd.melt(df_level, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Monetary Aggregates', value_name='level')

df_share = pd.melt(df_share, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Monetary Aggregates', value_name='share')

df_growth = pd.melt(df_growth, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Monetary Aggregates', value_name='growth')

df_contrib = pd.melt(df_contrib, id_vars=cols[0], value_vars=cols[1:],
                    var_name='Monetary Aggregates', value_name='contrib')

categories = df_level['Monetary Aggregates'].unique()


height = 600
width  = 700


# #A more beautiful racing graph here: https://towardsdatascience.com/bar-chart-race-with-plotly-f36f3a5df4f1

# dict_keys=['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen',
#            'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','twentyone','twentytwo',
#            'twentythree','twentyfour','twentyfive','twentysix','twentyseven','twentyeight', 'twentynine', 
#            'thirty'] 


# years=[1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 
#        1990, 1991,1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
#        2000, 2001, 2002,2003, 2004, 2005, 2006, 2007, 2008, 2009, 
#        2010,2011]

# n_frame={}

# for y, d in zip(years, dict_keys):
#     dataframe=df[(df['year']==y)&(df['indicator']=='sub_total')]
#     dataframe=dataframe.nlargest(n=12,columns=['share'])
#     dataframe=dataframe.sort_values(by=['year','share'])

#     n_frame[d]=dataframe

# fig=go.Figure(
#     data=[
#         go.Bar(
#         x=n_frame['one']['share'], y=n_frame['one']['Sectors'],orientation='h',
#         text=n_frame['one']['share'], texttemplate='%{text:.3s}',
#         textfont={'size':18}, textposition='inside', insidetextanchor='middle',
#         width=0.9, marker={'color':n_frame['one']['color_code']})
#     ],
#     layout=go.Layout(
#         xaxis=dict(range=[0, 60], autorange=False, title=dict(text='Share (in percent)',font=dict(size=18))),
#         yaxis=dict(range=[-0.5, 5.5], autorange=False,tickfont=dict(size=14)),
#         title=dict(text='Figure B3: Share (in percent) of Disbursement by Sector for Year: 1980',font=dict(size=28),x=0.5,xanchor='center'),
#         # Add button
#         updatemenus=[dict(type="buttons",
#           buttons=[dict(label="Play",
#             method="animate",
#             args=[None,{"frame": {"duration": 1000, "redraw": True}, "fromcurrent": True}]),
#           dict(label="Stop",
#             method="animate",
#             args=[[None],{"frame": {"duration": 0, "redraw": False}, 
#             "mode": "immediate","transition": {"duration": 0}}])])]
#     ),

#     frames=[
#             go.Frame(
#                 data=[
#                         go.Bar(x=value['share'], y=value['Sectors'],
#                         orientation='h',text=value['share'],
#                         marker={'color':value['color_code']})
#                     ],
#                 layout=go.Layout(
#                         xaxis=dict(range=[0, 60], autorange=False),
#                         yaxis=dict(range=[-0.5, 5.5], autorange=False,tickfont=dict(size=14)),
#                         title=dict(text='Figure B3: Share (in percent) of Disbursement by Sector for Year: '+str(value['year'].values[0]),
#                         font=dict(size=28))
#                     )
#             )
#         for key, value in n_frame.items()
#     ]
# )


dropdown = dbc.Card([
     dcc.Dropdown(
        id='id_aggregates',
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
 

# racing = dbc.Card([
#   dcc.Graph(
#         id='id_racing',
#         figure=fig,
#         config={'displaylogo': False}
#     ),

#     html.Small("Source: National Bank of Ethiopia"),       
       
#     ], 
#   body=True,
#  )
 

app.layout = html.Div([
  html.Br(),
  html.Br(),
  dbc.Row([
        dbc.Col(dropdown, md=12),
        dbc.Col(level, lg=6),
        dbc.Col(share, lg=6),
        dbc.Col(growth, lg=6),
        dbc.Col(contrib, lg=6),

        # dbc.Col(racing, lg=12),

  ]),
 
])


@app.callback(
    Output(component_id='id_level', component_property='figure'),
    [Input(component_id='id_aggregates', component_property='value')]
    )
def level(aggregates):
    dff_level = df_level[df_level['Monetary Aggregates'].isin(aggregates)]
    fig = px.area(dff_level, x= 'year',
                  y = 'level',
                  color='Monetary Aggregates',
                  title = "MS #1: Components of Money Supply(Billions of Birr)",
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
def growth(aggregates):
    dff_share = df_share[df_share['Monetary Aggregates'].isin(aggregates)]
    fig = px.line(dff_share, x= 'year',
                  y = 'share',
                  color='Monetary Aggregates',
                  title = "MS #2: Share of Components of Money Supply (Percent)",
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
def share(aggregates):
    dff_growth = df_growth[df_growth['Monetary Aggregates'].isin(aggregates)]
    fig = px.line(dff_growth, x= 'year',
                  y = 'growth',
                  color='Monetary Aggregates',
                  title = "MS #3: Growth Rate of Components of Money Supply (Percent)", 
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
    dff_contrib = df_contrib[df_contrib['Monetary Aggregates'].isin(aggregates)]
    fig = px.line(dff_contrib, x= 'year',
                  y = 'contrib',
                  color='Monetary Aggregates',
                  title = "MS #4: Contribution to Growth of Components of Money Supply (Percent)", 
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