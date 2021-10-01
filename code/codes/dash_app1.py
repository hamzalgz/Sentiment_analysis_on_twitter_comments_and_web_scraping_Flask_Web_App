import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv(r"C:\Users\lenovo\Desktop\flask_api\Code\sliceddata.csv")

app = dash.Dash(__name__)
df['length'] = df.txt.str.split().apply(len)
app.layout = html.Div([
    html.Div([
            html.Pre(children= "Distribution de la longueur des tweets en fonction de leur fréquences par leur polarité",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),
    html.Div([
        html.Label(['Distribution de la longueur des tweets selon leur polarité']),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                     {'label': 'Pour les commentaires positives', 'value': 4},
                     {'label': 'Pour les commentaires négatives', 'value': 0},
            ],
            value=0,
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        dcc.RadioItems(
        id='dist-marginal',
        options=[{'label': x, 'value': x} 
                 for x in ['box', 'violin', 'rug']],
        value='box'
    ),
        dcc.Graph(id='the_graph')
        
    ]),

])

#---------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')],
    [Input(component_id='dist-marginal', component_property='value')]
)

def update_graph(my_dropdown,marginal):
    dff = df

    fig = px.histogram(dff,x=dff['length'][dff.target == my_dropdown ],marginal=marginal)
    return (fig)


if __name__ == '__main__':
    app.run_server(debug=True)