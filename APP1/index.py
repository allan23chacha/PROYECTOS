from datetime import datetime
import dash
import dash_bootstrap_components as dbc
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
external_stylesheets = [dbc.themes.BOOTSTRAP]  
from dash import Dash, dcc, html,callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# bootstrap theme
# https://bootswatch.com/lux/
# external_stylesheets = [dbc.themes.SANDSTONE]

import pandas as pd
import numpy as np
app = Dash(__name__, suppress_callback_exceptions=True) #external_stylesheets=external_stylesheets
server = app.server
# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
tiempo =  datetime.now().time()

header = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("ALLAN"),className="columnas_fila"),
        dbc.Col(html.H2("CHACHA"),className="columnas_fila"),
        dbc.Col([
            dbc.Row(html.H2("HORA INGRESO ")),
            dbc.Row(html.H2(str(tiempo).split(".")[0]),className="hora")
        ],className="columnas_fila")
    ],className="linea_principal")
])
contenido1 = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row(html.H2("TALLER"),className="taller"),
            dbc.Row(html.Img(src = "https://i.ytimg.com/vi/BcI1mXLX7wY/maxresdefault.jpg"),className="row_imagen")
        ],className ="col1"),
        dbc.Col([
            dbc.Row(html.Video(src ="assets/video1.mp4",controls = True),className="linea_video")
            ],className ="col2")
    ],className="linea_principal")
])
linea_titulo = dbc.Container([
    dbc.Row(),
    dbc.Row([html.H2("MI PRIMERA PÁGINA")],className="TITULOp")
],className="container_title")

df = pd.read_csv("assets/datas/carros.csv",sep=",")
df["Num_carro"] = [f"Carro{x}" for x in np.arange(1,df.shape[0]+1)]
df["Tipocarro"] = [ "TESLA" if x%2==0 else "MAZDA" for x in np.arange(1,df.shape[0]+1)]
fig = px.scatter(df,x="kms",y="precio",title="KMS VS PRECIO",color="Tipocarro",hover_data="Num_carro")
fig.update_layout(
    xaxis_title="KMS",
    yaxis_title="PRECIO"
)

DataAnalisis = dbc.Container([
    dbc.Row(html.H1("Analisis del archivo Carros.csv"),className="TITULOp"),
    dbc.Row(dcc.Graph(figure=fig))
],className="container_analysis")

DataAnalisis2 = dbc.Container([
    dbc.Row(html.H1("Escoge un vehiculo"),className="TITULOp"),
    dbc.Row(dcc.Dropdown(
            df['Tipocarro'].unique(),
            value="MAZDA",
            id="selected_tipocarro",
    )),
    dbc.Row(dcc.Graph(id="figurafiltada1"))
],className="container_analysis")

@app.callback(
    Output("figurafiltada1","figure"),
    Input("selected_tipocarro","value")
)
def crear_figura_filtrada(tipocarro):
    df_filtrado = df[df["Tipocarro"]==tipocarro]
    fig = px.scatter(df_filtrado,x="kms",y="precio",title="KMS VS PRECIO",color="Tipocarro",hover_data="Num_carro")
    fig.update_layout(
        xaxis_title="KMS",
        yaxis_title="PRECIO",
    )
    return fig


app.layout = html.Div([
    header,contenido1,linea_titulo,DataAnalisis,DataAnalisis2
])


if __name__ == '__main__':
    app.run_server(host='127.0.0.1',port=8020 ,debug=True)



