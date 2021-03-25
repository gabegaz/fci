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
 
app.layout = html.Div([
	html.Br(),
	html.Br(),
	html.Center("Monitorying Ethiopian Financial Sector")
	]
)
