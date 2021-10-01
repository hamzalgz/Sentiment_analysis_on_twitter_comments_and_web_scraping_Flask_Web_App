import dash                              # pip install dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import plotly.express as px

from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from wordcloud import WordCloud  

df = pd.read_csv(r"C:\Users\hamza lagramez\Desktop\proj\ourdatafin.csv")
df['length'] = df.txt.str.split().apply(len)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout =dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='/static/img/image5.jpg')
            ],className='mb-2'),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div(id='none',children=[],style={'display': 'none'}),
                    html.H1('Dashboard')
                ])
            ]),
        ], width=9),
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ]),
        ], width=3),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                
                    html.Div([

                        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
                        dcc.Tab(label='Main Dashboard', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                        dcc.Tab(label='Longueur en fréquence', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                        dcc.Tab(label='Piechart', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                        dcc.Tab(label='Wordcloud', value='tab-4', style=tab_style, selected_style=tab_selected_style),
                        dcc.Tab(label='Longueur en densité', value='tab-5', style=tab_style, selected_style=tab_selected_style)
                    ], style=tabs_styles),
                    html.Div(id='tabs-content-inline')                 
                ])
            ]),
        ], width=12),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Distribution de la longueur des tweets en fonction de leur fréquence par leur polarité'),
                    dcc.Graph(id='histogramm1', figure={}, config={'displayModeBar': False}),
                    html.H6('click on Longueur en fréquence tab to see more')                 
                ])
            ]),
        ], width=12),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Piechart indiquant le pourcentage des tweets positives et négatives'),
                    dcc.Graph(id='pie-chart', figure={}),
                    html.H6('click on Piechart tab to see more')
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Wordcloud des mots des tweets'),
                    dcc.Graph(id='wordcloud', figure={}),
                    html.H6('click on wordcloud tab to see more')
                ])
            ]),
        ], width=6),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Distribution de la longueur des tweets en fonction de leur densité par leur polarité'),
                    dcc.Graph(id='histogramm2', figure={}, config={'displayModeBar': False}),
                    html.H6('click on Longueur en densité tab to see more') 
                ])
            ]),
        ], width=12),
    ],className='mb-2')
], fluid=True)

#Worldcloud-----------------------------------------

@app.callback(
    Output('wordcloud','figure'),
    Input('none','children')
)
def update_worldcloud(input):
    dff = df.copy()
    my_wordcloud = WordCloud(
        background_color='white',
        height=275
    ).generate(' '.join(dff["txt"]))

    fig_wordcloud = px.imshow(my_wordcloud, template='ggplot2')
    fig_wordcloud.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_wordcloud.update_xaxes(visible=False)
    fig_wordcloud.update_yaxes(visible=False)

    return fig_wordcloud

 #Histogramm1-----------------------------------------------   

@app.callback(
    Output('histogramm1','figure'),
    Input('none','children')
)
def update_histogramm(input):
    dff = df.copy()
    fig = px.histogram(dff,x=dff['length'][dff.target ==0 ])
    return (fig)

#pie-------------------------
@app.callback(
    Output('pie-chart','figure'),
    Input('none','children'),
    
)
def update_pie(tweet):
    dff = df.copy()
    fig_pie =px.pie(
        data_frame=dff,
        names=dff['target'],
        hole=.3,
        )
    fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_pie.update_traces(marker_colors=['red','blue'])

    return fig_pie

#Histogramm2----------------------------------------------- 
@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='length', component_property='value')])
def display_graph( tweet ):
    positive=df[df.target==tweet]
    x='negative'
    if tweet==0:
        pass
    else:
        x='positive'
    fig = ff.create_distplot(hist_data=[positive.length.values.tolist() ],group_labels=['distribution de longueur des tweets ' +x ])
    return( fig)

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Tab content 5')
        ])

if __name__=='__main__':
    app.run_server(debug=True)