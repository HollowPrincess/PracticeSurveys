import os

from dash.dependencies import Input, Output
import plotly.graph_objs as go
#from pandas_datareader import data as web
#from datetime import datetime as dt

"""
!pip install dash-table
"""

try:
    import dash
except ModuleNotFoundError:
    print ('You must install dash: pip install dash')
    sys.exit
    
try:
    import dash_core_components as dcc
except ModuleNotFoundError:
    print ('You must install dash-core-components: pip install dash-core-components')
    sys.exit
    
try:
    import dash_html_components as html  
except ModuleNotFoundError:
    print ('You must install dash-html-components: pip install dash-html-components')
    sys.exit
    

def assessmentsGraphs(surveysCounter,coursePortrait):
    os.chdir('..')
    
    assessmentOptions=[]
    for column in coursePortrait.columns:        
        if column.split(' ')[0]=='средняя':
            assessmentOptions.append({'label': column, 'value': column})
            
    sessionColors=[]
    for courseName in coursePortrait.курс:
        isSpecial=courseName.lower().find('спец.') #position of the substring or -1
        isSPBU=courseName.lower().find('спбгу')
        if isSpecial==-1:
            sessionColors.append('rgb(0,182,255)') #ordinary session is blue
        elif isSPBU!=-1:
            sessionColors.append('rgb(0,255,20)') #special spbu session is green
        else:
            sessionColors.append('rgb(254,204,2)') #special session of another universities is orange
            
    app = dash.Dash()    
    app.layout = html.Div(children=[
        html.Div(children='Количество обработанных анкет: '+str(surveysCounter)),
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
            options=assessmentOptions
        ),

        dcc.Graph(id='my-graph')
        
    ], style={'width': '1000','heigth':'1000'} )
   
    @app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        if not (selected_dropdown_value is None):
            graphName=selected_dropdown_value[0].upper()+selected_dropdown_value[1:]
            res={
                'data': [
                    {'x': coursePortrait.курс,
                     'y': coursePortrait[selected_dropdown_value],
                     'marker': {'color': sessionColors},
                     'type': 'bar', 
                     'name': graphName
                    }],
                'layout': {'title': graphName}
            }
        else:
            res={}
        return res
    
    app.run_server()