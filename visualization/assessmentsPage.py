import os
import sys
import pandas as pd
import plotly.plotly as py


from dash.dependencies import Input, Output
import plotly.graph_objs as go


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
    
def getBorderColors(coursePortrait, selected_dropdown_value):
    colors=[]
    for columnName in coursePortrait.columns:
        if columnName.find('рекомендуемый объем выборки для'+selected_dropdown_value)==-1:
            colors.append('white')
        else:
            colors.append('black')
    return colors
    

def assessmentsGraphs(df, surveysCounter,coursePortrait,avgErr):
    os.chdir('..')
    df=df.sort_values(by='курс')

    assessmentOptions=[]
    for column in df.columns:        
        if column.split(' ')[0]=='оценка':
            assessmentOptions.append({'label': column, 'value': column})
            
    sessionColorsInPortrait=[]
    for courseName in coursePortrait.курс:
        isSpecial=courseName.lower().find('спец.') #position of the substring or -1
        isSPBU=courseName.lower().find('спбгу')
        if isSpecial==-1:
            sessionColorsInPortrait.append('rgb(0,182,255)') #ordinary session is blue
        elif isSPBU!=-1:
            sessionColorsInPortrait.append('rgb(0,255,20)') #special spbu session is green
        else:
            sessionColorsInPortrait.append('rgb(254,204,2)') #special session of another universities is orange
     
        
    sessionColorsInDF=[]
    for courseName in df.курс:
        isSpecial=courseName.lower().find('спец.') #position of the substring or -1
        isSPBU=courseName.lower().find('спбгу')
        if isSpecial==-1:
            sessionColorsInDF.append('rgb(0,182,255)') #ordinary session is blue
        elif isSPBU!=-1:
            sessionColorsInDF.append('rgb(0,255,20)') #special spbu session is green
        else:
            sessionColorsInDF.append('rgb(254,204,2)') #special session of another universities is orange
    c=[]        
    for i in range(42):
        c.append('red')

            
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
        
        html.H2('Выберите графики:', className='row',
                            style={'padding-top': '20px'}),
        dcc.Dropdown(
            id='my-dropdown',
            options=assessmentOptions
        ),

        dcc.Graph(id='avggraph'),
        html.Div([html.P('На данном графике изображены средние оценки для каждого курса. Черным обведены нерелевантные данные - объем выборки является недостаточным для рассматриваемой оценки. Зеленым цветом выделены специальные сессии СПбГУ, желтым - другие специальные сессии, синим - все остальные сессии.', className='row', style={'padding-left': '30px','fontSize': 20})]),
        
        dcc.Graph(id='boxgraph'),
        
        dcc.Graph(id='allgraph'),
        html.Div([html.P('На данном графике отмечены все оценки, которые пользователи указывали для конкретного курса. Цветовая гамма точек выбрана по тому же принципу, что и на графике выше.', className='row',style={'padding-left': '30px','fontSize': 20})]),
        
    ], style={'width': '1000','heigth':'1000'} )
   
    @app.callback(Output('avggraph', 'figure'), [Input('my-dropdown', 'value')])
    def update_avggraph(selected_dropdown_value):
        if not (selected_dropdown_value is None):
            assessmentName=selected_dropdown_value[len('оценка'):]
            lineColors=coursePortrait['рекомендуемый объем выборки для средней оценки'+assessmentName+' при отклонении '+str(avgErr)]
            graphName='Средняя '+selected_dropdown_value          
            res={
                'data': [
                    {'x': coursePortrait.курс,
                     'y': coursePortrait['средняя '+selected_dropdown_value],
                     'marker': {
                         'color': sessionColorsInPortrait, 
                         'line': {'width': 1, 'color': lineColors}
                     },                     
                     'type': 'bar', 
                     'name': graphName
                    }],
                'layout': {'title': graphName}
            }
        else:
            res={}
        return res
    
    @app.callback(Output('allgraph', 'figure'), [Input('my-dropdown', 'value')])
    def update_allgraph(selected_dropdown_value):
        if not (selected_dropdown_value is None):
            assessmentName=selected_dropdown_value[selected_dropdown_value.find('оценка'):]
            graphName=assessmentName[0].upper()+assessmentName[1:]            
            res={
                'data': [
                    go.Scatter(
                        x=df.курс,
                        y=df[assessmentName],                        
                        mode='markers',
                        opacity=1,
                        marker={
                            'color': sessionColorsInDF,
                            'size': 8                            
                        },
                    ) 
                ],
                'layout': {'title': graphName}
            }
        else:
            res={}
        return res
    
    @app.callback(Output('boxgraph', 'figure'), [Input('my-dropdown', 'value')])
    def update_boxgraph(selected_dropdown_value):
        if not (selected_dropdown_value is None):
            assessmentName=selected_dropdown_value[selected_dropdown_value.find('оценка')+len('оценка'):]            
            graphName='Диаграмма размаха '+selected_dropdown_value 
            res={
                'data': [
                    go.Box(
                        name=coursePortrait.курс[i],
                        y=df['оценка'+assessmentName],                        
                        
                        marker={
                            'color': sessionColorsInPortrait[i]              
                        },
                    ) for i in range(len(sessionColorsInPortrait))
                ],
                'layout': {'title': graphName}
            }
            
        else:
            res={}
        return res
    
    app.run_server(debug=True)