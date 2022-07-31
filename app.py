from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Lectura de archivo
df = pd.read_csv('https://raw.githubusercontent.com/wagamezj/prueba_xepelin/main/data_test%20(1).csv', sep = ';')
# Se seleccionan solo las transacciones validas que me generan una fecha
df = df[df.status == 'PAID']
# Cambio de la estructura de la fecha
df['paidAt'] =  pd.to_datetime(df['paidAt'])
#df['paidAt'] = df['paidAt'].fillna('0/0/0 00:00', inplace=True) # Cambio si necesito realizar analisis sobre transacciones en proceso
# Genero la variable mes
df['mes_id'] =  df['paidAt'].dt.strftime('%Y-%m')
# Calculo del porcentaje de financiación
df['finan'] = df.amountfinancedByXepelin/df.amount


# Codigo Grafico 1
fin_mounth = df.groupby('mes_id').agg({'amountfinancedByXepelin':[sum],'amount':[sum]})
fin_mounth.columns = fin_mounth.columns.droplevel(level=1)
fin_mounth = fin_mounth.reset_index()
fin_mounth['finan'] = fin_mounth.amountfinancedByXepelin / fin_mounth.amount


fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(
    x=fin_mounth['mes_id'],
    y=fin_mounth['amount'],
    name='Monto total transado',
    marker_color='blue'
))

fig.add_trace(go.Scatter(x=fin_mounth['mes_id'], y=fin_mounth['finan'],
                    mode='lines',
                    name='Porcentaje de Financiacion' ),
                    secondary_y= True,
             )


fig.update_layout(
    title_text="Relación monto vs Financiación"
)

# Codigo Grafico 2
fig2 = go.Figure()
fin_mounth = df.groupby('mes_id')['amountfinancedByXepelin'].sum().reset_index()
fig2 = px.bar(fin_mounth, x = 'mes_id', y = 'amountfinancedByXepelin' )


# Codigo grafico 3
fig3 = go.Figure()
client2 = df.groupby('PayerId')['amountfinancedByXepelin'].sum().reset_index()
fig3 = px.bar(client2, x = 'PayerId', y = 'amountfinancedByXepelin')

# Codigo grafico 4

# Estadisticos historicos de clientes
client = df.groupby('PayerId').agg({'amountfinancedByXepelin':[sum],'amount':['sum'] ,'PayerId':['count']})
client.columns = client.columns.droplevel(level=1)
client = client.rename(columns={'PayerId':'freq'}).reset_index()
client['Ind_fina'] = client.amountfinancedByXepelin/client.amount
client.sort_values(by=['amount'], inplace=False,ascending=False)
fig4 = go.Figure()
fig4 = px.bar(client, x = 'PayerId', y = 'freq')

# Codigo grafico 5

mes = ['2021-02','2021-03','2021-04','2021-05','2021-06','2021-07','2021-08','2021-09']
acumulado = []
nuevos_id = []
for i in mes:
    new = df[df['mes_id'] == i]
    nuevas = new.PayerId.unique()
    conteo = 0
    for j in nuevas:
        if j not in acumulado:
            conteo += 1
            acumulado += j ,
    nuevos_id += conteo ,
    
fig5 = go.Figure()

fig5.add_trace(go.Scatter(x=mes, y=nuevos_id,
                    mode='lines',
                    name='Porcentaje de Financiacion' ),
                    )


fig5.update_layout(
    title_text="Clientes nuevos mes"
)


# Codigo Figura 6

serie1 = df.groupby(['paidAt','mes_id'])['amount'].sum().reset_index()
fig6 = px.line(serie1, x='paidAt', y="amount")


app = Dash(__name__)


colors = {
    'background': '#f8f8ff',
    'text': '#0000FF'
}


app.layout = html.Div(
    
    style={'backgroundColor': colors['background'],'width': '100%'}, children=[
        
        html.Img(
        src='xepelin_horizontal.jpg'
        
        ),
        html.H1(
        children='DASH DESCRIPCION TRANSACCIONES',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Wilmer Jesus Agamez Julio', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
        
    html.Div([
         dcc.Graph(
            id='grafica1',
            figure=fig)], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
     html.Div([
         dcc.Graph(
            id='grafica2',
            figure=fig2)], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
         dcc.Graph(
            id='grafica3',
            figure=fig3)], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
     html.Div([
         dcc.Graph(
            id='grafica4',
            figure=fig4)], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
     html.Div([
         dcc.Graph(
            id='grafica5',
            figure=fig5)], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
         dcc.Graph(
            id='grafica6',
            figure=fig6)], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})
    
        
    ,
])




if __name__ == '__main__':
    app.run_server()