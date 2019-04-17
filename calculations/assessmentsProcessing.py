import numpy as np
import pandas as pd

def recommendedSampleSize(x,avgErr,minimumSampleSize):
    return max(round(pow(np.std(x)/avgErr,2)),minimumSampleSize)

def countAvgAndSizeForAssessment(assessmentName,df,avgErr,minimumSampleSize):
    newColInPortrait=df.groupby(['курс']).agg({
        'оценка '+assessmentName:[np.average , lambda x:recommendedSampleSize(x,avgErr,minimumSampleSize)]
    })
    newColInPortrait=newColInPortrait.rename(index=str, 
                                     columns={'average': 'средняя оценка '+assessmentName,
                                              '<lambda>':'рекомендуемый объем выборки для средней оценки '+assessmentName+' при отклонении '+str(avgErr)
                                             })
    newColInPortrait.columns=newColInPortrait.columns.droplevel(level=0)
    return newColInPortrait

def assessmentsProcessing(df,avgErr,minimumSampleSize):    
    coursePortrait=df.groupby(['курс']).agg({'оценка содержания курса':[np.size]})
    coursePortrait=coursePortrait.rename(index=str, 
                                         columns={'size':'количество отзывов на курс'})
    coursePortrait.columns=coursePortrait.columns.droplevel(level=0)
    
    
    for column in df.columns:
        if column.split(' ')[0]=='оценка':
            assessmentName=column.split(' ')[1:]
            assessmentName=' '.join(map(str, assessmentName))
            frames = [countAvgAndSizeForAssessment(assessmentName,df,avgErr,minimumSampleSize),coursePortrait]
            coursePortrait=pd.concat(frames,axis=1)
            
    coursePortrait=coursePortrait.reset_index()
    
    coursePortraitCopy=coursePortrait['количество отзывов на курс'].copy(deep=True)
    coursePortrait['количество отзывов на курс']=coursePortrait['количество отзывов на курс'].where(30<coursePortrait['количество отзывов на курс'], coursePortrait['количество отзывов на курс']-1)
    for columnName in coursePortrait.columns:
        if columnName.find('рекомендуемый объем выборки для средней оценки')!=-1:
            coursePortrait[columnName]=coursePortrait[columnName].where(coursePortrait[columnName]<=coursePortrait['количество отзывов на курс'], 'black')
            coursePortrait[columnName]=coursePortrait[columnName].where(coursePortrait[columnName]=='black', 'white')
    coursePortrait['количество отзывов на курс']=coursePortraitCopy
    return coursePortrait