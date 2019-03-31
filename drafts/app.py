import dash
import dash_core_components as dcc
import dash_html_components as html    
import pandas as pd
import os
import numpy as np

os.chdir('surveys')
df = pd.read_csv('surveys.csv', sep=',', encoding='utf-8', parse_dates=['Отметка времени'], 
                 dayfirst=True) 
df=df.rename(index=str, columns={
    "Отметка времени": "время",
    "Название курса": "курс",
    "1. Оцените, пожалуйста, содержание курса по пятибалльной шкале, где «очень нравится» - 5 баллов, «совсем не нравится» - 1 балл [Содержание курса]": "оценка содержания курса",
    "1. Оцените, пожалуйста, содержание курса по пятибалльной шкале, где «очень нравится» - 5 баллов, «совсем не нравится» - 1 балл [Структура курса]": "оценка структуры курса",
    "1. Оцените, пожалуйста, содержание курса по пятибалльной шкале, где «очень нравится» - 5 баллов, «совсем не нравится» - 1 балл [Визуальная составляющая]": "оценка визуальной составляющей",
    "Напишите, пожалуйста, свое мнение о курсе:": "мнение о курсе",
    "Оцените, пожалуйста, преподавателя\авторский коллектив по следующим критериям: [Подача материала]": "оценка подачи материала авторами",
    "Оцените, пожалуйста, преподавателя\авторский коллектив по следующим критериям: [Активность в общении со слушателями]": "оценка активности авторов",
    "Оцените, пожалуйста, преподавателя\авторский коллектив по следующим критериям: [Компетентность]": "оценка компетентности авторов",
    "Напишите, пожалуйста, свое мнение о преподавателе:": "мнение о преподавателе",
    "Оцените, пожалуйста, рост интереса к курсу по мере его прохождения по пятибалльной шкале, где стабильно рос - 5 баллов, стабильно падал - 1 балл [Интерес к курсу]": "оценка уровеня интереса к курсу во времени",
    "Оцените задания и дополнительные материалы к курсу по пятибалльной шкале, где «очень помогли в приобретении нужных компетенций» - 5, «совершенно не помогли» - 1 балл [Задания к курсу]": "оценка заданий к курсу",
    "Оцените задания и дополнительные материалы к курсу по пятибалльной шкале, где «очень помогли в приобретении нужных компетенций» - 5, «совершенно не помогли» - 1 балл [Дополнительные материалы]": "оценка дополнительных материалов",
    "Напишите, пожалуйста, свое мнение о материалах курса:": "мнение о материалах",
    "Довольны ли вы в целом пройденным курсом по 10-балльной шкале, где 10 баллов «очень доволен», 1 балл – «категорически недоволен»": "оценка уровня удовлетворенности",
    "Будете ли рекомендовать курсы СПбГУ другим": "согласие рекомендовать",
    "Ваши предложения по улучшению курса": "предложения",
    "Являетесь ли вы студентом": "студент"    
})
df=df.rename(str.lower, axis='columns')

df['оценка подачи материала авторами'] = df['оценка подачи материала авторами'].map({'Очень плохо': 1, 'Плохо': 2,'Удовлетворительно': 3, 'Хорошо': 4,'Отлично': 5})
df['оценка активности авторов'] = df['оценка активности авторов'].map({'Очень плохо': 1, 'Плохо': 2,'Удовлетворительно': 3, 'Хорошо': 4,'Отлично': 5})
df['оценка компетентности авторов'] = df['оценка компетентности авторов'].map({'Очень плохо': 1, 'Плохо': 2,'Удовлетворительно': 3, 'Хорошо': 4,'Отлично': 5})

#make categories yes/no to 1/0
df['согласие рекомендовать'] = df['согласие рекомендовать'].map({'Да': 1, 'Нет': 0})
df['студент'] = df['студент'].map({'Да': 1, 'Нет': 0})
# make sex to isMale:
df=df.rename(index=str, columns={"пол": "мужчина?"})
df['мужчина?'] = df['мужчина?'].map({'М': 1, 'Ж': 0})

# a portrait of each course
# num of votes
# avg asessments
# num of male and female votes
# how many users want to recommend a course


# data representativeness estimate
avgErr=0.25 #param

def recommendedSampleSize(x):
  return round(pow(np.std(x)/avgErr,2))

coursePortrait=df.groupby(['курс']).agg({'оценка содержания курса':[np.size]})
coursePortrait=coursePortrait.rename(index=str, 
                                     columns={'size':'количество отзывов на курс'})
coursePortrait.columns=coursePortrait.columns.droplevel(level=0)


def countAvgAndSizeForAssessment(assessmentName):
    newColInPortrait=df.groupby(['курс']).agg({
        'оценка '+assessmentName:[np.average , lambda x:recommendedSampleSize(x)]
    })
    newColInPortrait=newColInPortrait.rename(index=str, 
                                     columns={'average': 'средняя оценка '+assessmentName,
                                              '<lambda>':'рекомендуемый объем выборки для оценки '+assessmentName+' при отклонении '+str(avgErr)
                                             })
    newColInPortrait.columns=newColInPortrait.columns.droplevel(level=0)
    return newColInPortrait




for assessmentName in df.columns:
    if assessmentName.split(' ')[0]=='оценка':
        newName=assessmentName.split(' ')[1:]
        newName=' '.join(map(str, newName))
        frames = [countAvgAndSizeForAssessment(newName),coursePortrait]
        coursePortrait=pd.concat(frames,axis=1)
        
coursePortrait=coursePortrait.reset_index()

os.chdir('..')
app = dash.Dash()
 
app.layout = html.Div(children=[
html.Div(children='Surveys report'),
dcc.Graph(
id='количество отзывов',
figure={
'data': [
{'x':coursePortrait.курс, 'y':coursePortrait['количество отзывов на курс'], 'type':'bar', 'name':'Количество отзывов'},
],
'layout': {
'title': 'График количества отзывов на каждый курс'
}
}
),
dcc.Graph(
id='количество отзывов2',
figure={
'data': [
{'x':coursePortrait.курс, 'y':coursePortrait['средняя оценка содержания курса'], 'type':'bar', 'name':'Средняя оценка содержания курса'},
],
'layout': {
'title': 'График средней оценки содержания курса'
}
}
)
])
 
if __name__ == '__main__':
    app.run_server(debug=True)