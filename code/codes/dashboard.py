from dash_html_components.H6 import H6
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.figure_factory as ff
from wordcloud import WordCloud 
import dash_bootstrap_components as dbc
import dash_table


import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
from dash_extensions import Lottie  
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import date
import calendar
from wordcloud import WordCloud          # pip install wordcloud
app=dash.Dash(__name__)

# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])


df=pd.read_csv(r'D:/project twee/proj/ourdatafin.csv')
dff=df[['txt','target']]
dfff=dff.copy()
    
url_coonections = "https://assets9.lottiefiles.com/private_files/lf30_5ttqPi.json"
url_companies = "https://assets9.lottiefiles.com/packages/lf20_EzPrWM.json"
url_msg_in = "https://assets9.lottiefiles.com/packages/lf20_8wREpI.json"
url_msg_out = "https://assets2.lottiefiles.com/packages/lf20_Cc8Bpg.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

df['length'] = df.txt.str.split().apply(len)
    
tabs_styles = {
    'height': '44px'
}

tabs_styles = {
    'height': '44px',
    'align-items': 'center'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#F2F2F2',
    'box-shadow': '4px 4px 4px 4px lightgrey',

}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'border-radius': '15px',
}
colors = {
    'background': '#FFFAF0',
    'text': '#7FDBFF'
}
dash_app.layout =  html.Div(style={'backgroundColor': colors['background']}, children=[ 
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardImg(src='/static/img/twitteree.png')
                ],className='mb-2'),
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id='none',children=[],style = {'backgroundColor': colors['background']}),
                        html.H1('Dashboard',style ={'color': '#0000CD'}),
                        html.H6('realise par menani abdelkabir et hamza lagramez')
                    ])
                ]),
            ], width=9),
        ],className='mb-2 mt-2'),

        dbc.Row([
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(Lottie( options=options,width="67%", height="67%", url=url_coonections)),
                    dbc.CardBody([
                        html.H6('replies count'),
                        html.H2(id='content-companies', children=str(42))
                    ], style={'textAlign':'center'})
                ]),
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(Lottie( options=options,width="67%", height="67%", url=url_companies)),
                    dbc.CardBody([
                        html.H6('likes'),
                        html.H2(id='content-msg-in', children="396")
                    ], style={'textAlign':'center'})
                ]),
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_msg_in)),
                    dbc.CardBody([
                        html.H6('quote tweets'),
                        html.H2(id='content-msg-out', children="19")
                    ], style={'textAlign': 'center'})
                ]),
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_msg_out)),
                    dbc.CardBody([
                        html.H6('retweets'),
                        html.H2(id='content-reactions', children="49")
                    ], style={'textAlign': 'center'})
                ]),
            ], width=2),
        ],className='mb-2'),
        
        dbc.Row([
            dbc.Col([
                    
                dcc.Tabs([


                    dcc.Tab(label='table', children=[ 
                        html.Div([
                            html.H3('tableau de prediction')
                        ]),
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in dfff.columns],
                            
                            data=dfff.to_dict('records'),
                        )],style = tab_style, selected_style = tab_selected_style),

                    dcc.Tab(label='word cloud', children=[ 
                           
                            dbc.Row([   ], className='mb-3'),  
                            dbc.Col([dcc.Dropdown(
                                id='len',
                                options=[{'label': 'tweets positives', 'value': 4}, 
                                        {'label': 'tweets negatives', 'value': 0}
                                    ],
                                
                                value=0,
                                style={'width' : '50%',
                                    'text-align': 'center',
                                    }
                                
                            ),
                    
                            
                            ] ,width={"size": 10, "order": 1, "offset": 4},className='mb-2'),
                            dbc.Col([

                            dcc.Graph(id="wordcloud",figure={'layout':{'height':450,'width':550,'paper_bgcolor': colors['background']}})],width={"size": 10, "order": 1, "offset": 3},className='mb-2')
                        ],style = tab_style, selected_style = tab_selected_style),


                

                    dcc.Tab(label='distplot', children=[   
                        

                        dbc.Row([   ], className='mb-3'),        
                        dbc.Col([dcc.Dropdown(
                            id='length',
                            options=[{'label': 'tweets positives', 'value': 4}, 
                                    {'label': 'tweets negatives', 'value': 0}
                                ],
                            
                            value=0,
                            style={"width": "50%"}
                        ), 
                        ],width={"size": 10, "order": 1, "offset": 4},className='mb-2'),
                        dcc.Graph(id='display', figure={'layout':{'height':1000}})
                        
                        ],style = tab_style, selected_style = tab_selected_style),




                    dcc.Tab(label='pie', children=[ 
                        html.Div([
                            html.H3('pie chart des nouveaux donnees devise en deux categories positive et negative')
                        ]),
                        dcc.Graph(id="pie-chart"  ,figure={'layout':{'title': 'Rank'}})
                        ], style = tab_style, selected_style = tab_selected_style),




                    dcc.Tab(label='histogram', children=[   
                        
                        dbc.Row([   ], className='mb-3'),        
                        dbc.Col([dcc.Dropdown(
                                id='len1',
                                options=[{'label': 'tweets positives', 'value': 4}, 
                                        {'label': 'tweets negatives', 'value': 0}
                                    ],
                                
                                value=0,
                                style={"width": "50%"}
                            ), 

                            dbc.CardBody([
                            dcc.RadioItems(
                                id='dist-marginal',
                                options=[
                                    {'label': ' box    __', 'value': 'box'},
                                    {'label': '  violin   __', 'value': 'violin'},
                                    {'label': '  rug', 'value': 'rug'}

                                ],
                                value='box'
                                ),
                            ]),


                            ],width={"size": 10, "order": 1, "offset": 4},className='mb-2'),
                            dcc.Graph(id='histogram', figure={}, config={'displayModeBar': False})
                        
                        ],style = tab_style, selected_style = tab_selected_style),

                    ],style = tabs_styles),


            ],width={"size": 10 ,'order':3, "offset": 1}),
        ], className='mb-2')
    ], fluid=True)])
#Worldcloud-----------------------------------------

@dash_app.callback(
    Output('wordcloud','figure'),
    [Input(component_id='len', component_property='value')]
)
def update_worldcloud( tweet):
    dff = df.copy()
    my_wordcloud = WordCloud(
        background_color='white',
        height=275
    ).generate(' '.join(dff['txt'][dff.target == tweet ]))

    fig_wordcloud = px.imshow(my_wordcloud, template='ggplot2')
    fig_wordcloud.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_wordcloud.update_xaxes(visible=False)
    fig_wordcloud.update_yaxes(visible=False)

    return fig_wordcloud


#histogram---------------------------------------------------------------
@dash_app.callback(
    Output(component_id='display', component_property='figure'),
    [Input(component_id='length', component_property='value')])
def display_graph( tweet ):
    positive=df[df.target==tweet]
    x='negative'
    if tweet==0:
        pass
    else:
        x='positive'
    fig = ff.create_distplot(hist_data=[positive.length.values.tolist() ],group_labels=['les tweets ' +x ])
    return( fig)


#pie-------------------------
@dash_app.callback(
    Output('pie-chart','figure'),
    Input('none','children'),
    
)
def update_pie(tweet):
   
    dff = df.copy()

 
    fig_pie =px.pie(
        data_frame=dff,
        names='target',
        hole=.3,
        )
   
    fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_pie.update_traces(marker_colors=['red','blue'])

    return fig_pie


#histogram---------------------------------------------------------------
@dash_app.callback(
    Output(component_id='histogram', component_property='figure'),
    [Input(component_id='len1', component_property='value')],
    [Input(component_id='dist-marginal', component_property='value')]
)

def update_graph(my_dropdown,marginal):
    dff = df

    fig = px.histogram(dff,x=dff['length'][dff.target == my_dropdown ],marginal=marginal)
    return (fig)


    #table---------------------------------------------------------------
@dash_app.callback(
    Output(component_id='table', component_property='figure'),
    Input('none','children'))
def table( tweet ):
    dff=df.copy()
    dff_s=dff[['txt','target']]
    d=dff_s[0:5]
    fig = ff.create_table(d)
    fig.show()


if __name__=='__main__':
    dash_app.run_server(debug=True)


   