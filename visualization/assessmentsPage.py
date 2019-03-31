import os

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
    app = dash.Dash()
    
    app.layout = html.Div(children=[
        html.Div(children='Surveys report'),
        
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
        dcc.Graph(
            id='оценки',
            figure={
                'data': [
                    {'x':coursePortrait.курс, 
                     'y':coursePortrait['средняя оценка содержания курса'], 
                     'type':'bar', 
                     'name':'Средняя оценка содержания курса'
                    },
                ],
                'layout': {'title': 'График средней оценки содержания курса'}
            }
        )
    ])
    
    #if __name__ == '__main__':
    app.run_server(debug=True)