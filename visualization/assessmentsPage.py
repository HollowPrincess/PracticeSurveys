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
    if __name__ == '__main__':
        app.run_server(debug=True)