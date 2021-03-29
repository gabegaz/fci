# -*- coding: utf-8 -*-

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from django_plotly_dash import DjangoDash
import dash_table as dt

app = DjangoDash('Dashboard', add_bootstrap_links=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
 



body = dbc.Container([ 
dbc.Row(
            [
            html.H5("Ethiopian financial sector monitoring ...")
            ], justify="center", align="center", className="h-50"
            )
],style={"height": "40vh", "color": "green"}

)


app.layout = html.Div([body])


