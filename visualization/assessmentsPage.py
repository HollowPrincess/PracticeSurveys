import os

from dash.dependencies import Input, Output
#from pandas_datareader import data as web
#from datetime import datetime as dt

"""
!pip install dash-table
"""

try:
    import dash
except ModuleNotFoundError:
    print ('You must install dash: pip install dash')
    #sys.exit
    
try:
    import dash_core_components as dcc
except ModuleNotFoundError:
    print ('You must install dash-core-components: pip install dash-core-components')
    #sys.exit
    
try:
    import dash_html_components as html  
except ModuleNotFoundError:
    print ('You must install dash-html-components: pip install dash-html-components')
    #sys.exit
    

def assessmentsGraphs(coursePortrait):
    os.chdir('..')
    
    assessmentOptions=[]
    for column in coursePortrait.columns:        
        if column.split(' ')[0]=='средняя':
            assessmentOptions.append({'label': column, 'value': column})
            
    app = dash.Dash()    
    app.layout = html.Div(children=[
        html.Div(children='Отчет по отзывам на курсы'),
        dcc.Graph(
            id='количество отзывов',
            figure={
                'data': [
                    {'x':coursePortrait.курс, 
                     'y':coursePortrait['количество отзывов на курс'], 
                     'type':'bar', 
                     'name':'Количество отзывов'
                    },
                ],
                'layout': {'title': 'График количества отзывов на каждый курс'}
            }
        ),
        html.H4('Выберите график:', className='row',
                            style={'padding-top': '20px'}),
        dcc.Dropdown(
            id='my-dropdown',
            options=assessmentOptions,
            value=assessmentOptions[0]
        ),

        dcc.Graph(id='my-graph')
        
    ], style={'width': '1000','heigth':'1000'} )
   
    @app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        return {
            'data': [
                {'x': coursePortrait.курс,
                'y': coursePortrait[selected_dropdown_value],
                'type': 'bar', 
                'name': selected_dropdown_value
            }],
            'layout': {'title': selected_dropdown_value}
        }
    
    app.run_server()