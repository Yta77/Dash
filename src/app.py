from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import datetime
import pandas_datareader.data as web
#from openpyxl.workbook import web

#Definizione Variabili (KPI & KRI)

PnL= pd.read_excel("PnL.xlsx")

Somma_PnL=PnL['PnL'].sum()
Somma_Exposure=PnL['Exposure_Mwh'].sum()
Somma_VaR=PnL['VaR'].sum()

#CARD



summary = {"P&L": "€100K", "VaR": "$5K",
           "Account Balance": "€600K", "Margin Change": "-€300K"}
def make_card(title, amount):
    return dbc.Card(
        [
            dbc.CardHeader(html.H2(title)),
            dbc.CardBody(html.H3(amount, id=title)),
        ],
        className="text-center shadow",
    )


#------------------------------------DATI CAPTURING GAS------------------------


df = pd.read_excel("Gas-prices-728.xlsx",sheet_name='PSV MW',usecols=["Data","BoM","BoW","Day ahead","WDNW","Month ahead"])

dff= pd.read_excel("Gas-prices-728.xlsx",sheet_name='TTF MW',usecols=["Data","BoM","BoW","Day ahead","WDNW","Month ahead"])

dfff=pd.merge(df,dff[["Data","BoM","BoW","Day ahead","WDNW","Month ahead"]],on='Data',how='right')

dfff.head()

dfff.rename(columns={'BoM_x': 'BoM_PSV', 'Day ahead_x': 'Day ahead_PSV','WDNW_x':'WDNW_PSV','Month ahead_x':'Month ahead_PSV','BoM_y': 'BoM_TTF', 'Day ahead_y': 'Day ahead_TTF','WDNW_y':'WDNW_TTF','Month ahead_y':'Month ahead_TTF'}, inplace=True)

# ------------------------------------DATA E ANNO------------------------------

data_excel=dfff['Data']

anno=data_excel.dt.year
dfff["Anno1"]=anno

dfff.rename(columns={'Anno1':'Anno1','BoM_x': 'BoM_PSV', 'Day ahead_x': 'Day ahead_PSV','WDNW_x':'WDNW_PSV','Month ahead_x':'Month ahead_PSV','BoM_y': 'BoM_TTF', 'Day ahead_y': 'Day ahead_TTF','WDNW_y':'WDNW_TTF','Month ahead_y':'Month ahead_TTF'}, inplace=True)
Test= dfff.query('Anno1==2023')


Test.info()
print(Test[:10])



app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB,dbc.icons.BOOTSTRAP],

                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server


app.layout = dbc.Container([

 #------------------------------------- RIGA 0 CARDS------------------------------

dbc.Row(

        [dbc.Col(make_card(k, v)) for k, v in summary.items()],
                  className="my-4"),


#-------------------------------------- E C O N O M I C S------------------------------

dbc.Row([
    dbc.Col(html.H1("Economics",
                    className='text-center text-primary mb-4'),
            width=10),

            (html.Div(

            [html.H4("Equity Line"),
             dcc.Graph(id="Equity"),
             html.P("Select Product:"),

             dcc.Dropdown(
                 id="pippo2",
                 options=["VaR", "PnL"],
                 multi=True,
                 value="VaR",
                 clearable=False,
                     ),
                                ]
                                     )
                                            )],
                #    xs=12, sm=12, md=12, lg=5, xl=5
                                                            ),

        dbc.Col(html.H1("Market Trend",
                               className='text-center text-primary mb-4'),
                                  width=10),


 #------------------------------------RIGA 1 GRAFICI MERCATO------------------------------

dbc.Row([

        dbc.Col([
                    (html.Div(

                    [html.H4("Gas Market Spot"),
                    dcc.Graph(id="time-series-chart"),
                    html.P("Select Product:"),

                dcc.Dropdown(
                    id="pippo",
                    options=["BoM_PSV", "Day ahead_PSV","WDNW_PSV","Month ahead_PSV","BoM_TTF", "Day ahead_TTF","WDNW_TTF","Month ahead_TTF"],
                    multi=True,
                    value="Day ahead_PSV",
                    clearable=False,
                            ),
                                 ]
                                    )
                                        )]),
# ------------------------------------------COLONNA 2------------------------------------

                dbc.Col([
                   (html.Div(
                   [html.H4("Power Market Spot"),
                   dcc.Graph(id="power_mkt"),
                   html.P("Select Product:"),

                dcc.Dropdown(
                  id="pw",
                  options=["BoM_PSV", "Day ahead_PSV","WDNW_PSV","Month ahead_PSV","BoM_TTF", "Day ahead_TTF","WDNW_TTF","Month ahead_TTF"],
                    multi=True,
                    value="Day ahead_PSV",
                    clearable=False,
                           )

                                            ])
                                                )])
                                                   ])
                                                     ] )


# ------------------------------------GRAFICO 1------------------------------

@app.callback(
    Output('Equity','figure'),
    Input('pippo2', 'value')

)


def display_time_series(pippo2):
    fig3 = px.bar(PnL, x="year", y=pippo2)
    fig3.update_xaxes(rangeslider_visible=True)
    return fig3

# -------------------------------------GRAFICO 2------------------------------------------

@app.callback(
    Output('time-series-chart','figure'),
    Input('pippo', 'value')

)

def display_time_series(pippo):
    fig = px.line(Test, x="Data", y=pippo)
    fig.update_xaxes(rangeslider_visible=True)
    return fig


# ------------------------------------GRAFICO 3------------------------------

@app.callback(
    Output('power_mkt','figure'),
    Input('pw', 'value')
)

def display_time_series(pw):
   fig2= px.line(Test, x="Data", y=pw)
   fig2.update_xaxes(rangeslider_visible=True)
   return fig2


if __name__ == "__main__":
    app.run_server(debug=True)
