import numpy as np
import pandas as pd

def recommendedSampleSize(x,avgErr):
    return round(pow(np.std(x)/avgErr,2))

def countAvgAndSizeForAssessment(assessmentName,df,avgErr):
    newColInPortrait=df.groupby(['курс']).agg({
        'оценка '+assessmentName:[np.average , lambda x:recommendedSampleSize(x,avgErr)]
    })
    newColInPortrait=newColInPortrait.rename(index=str, 
                                     columns={'average': 'средняя оценка '+assessmentName,
                                              '<lambda>':'рекомендуемый объем выборки для оценки '+assessmentName+' при отклонении '+str(avgErr)
                                             })
    newColInPortrait.columns=newColInPortrait.columns.droplevel(level=0)
    return newColInPortrait

def assessmentsProcessing(df,avgErr):
    coursePortrait=df.groupby(['курс']).agg({'оценка содержания курса':[np.size]})
    coursePortrait=coursePortrait.rename(index=str, 
                                         columns={'size':'количество отзывов на курс'})
    coursePortrait.columns=coursePortrait.columns.droplevel(level=0)
    
    for column in df.columns:
        if column.split(' ')[0]=='оценка':
            assessmentName=column.split(' ')[1:]
            assessmentName=' '.join(map(str, assessmentName))
            frames = [countAvgAndSizeForAssessment(assessmentName,df,avgErr),coursePortrait]
            coursePortrait=pd.concat(frames,axis=1)
            
    coursePortrait=coursePortrait.reset_index()
    
    return coursePortrait