import os
import pandas as pd

import fileDownloading
from dataPreparation import dataPreparation
from calculations import assessmentsProcessing
from calculations import textProcessing
from visualization import assessmentsPage
    
#settings

isFileNeedToBeDownloaded=False 
avgErr=0.25 #отклонение среднего значения 
minimumSampleSize=10


# if programm running from Collaboratory set True 
# if you need to refresh file set True

if (isFileNeedToBeDownloaded or (not (os.path.exists(os.getcwd()+'surveys/surveys.csv') 
            or os.path.exists(os.getcwd()+'//surveys//surveys.csv')))):
    
    isZip=False # if file with surveys has zip format set True
    docId='none' # set docId in Google drive (part of the link)
    
    fileDownloading.downloadingFromGoogleDrive(docId,isZip)
else:
    os.chdir('surveys')
    
df = pd.read_csv('surveys.csv', sep=',', encoding='utf-8', 
                 parse_dates=['Отметка времени'], 
                 dayfirst=True)

surveysCounter=df.shape[0]

df=dataPreparation.dataPreparation(df) #if a survey was changed this function need to be fixed

minimumSampleSize=minimumSampleSize-1
coursePortrait=assessmentsProcessing.assessmentsProcessing(df,avgErr,minimumSampleSize)

textFields=[]
for column in df.columns:
    if column.split(' ')[0]=='мнение':
        textFields.append(column)
textFields.append('предложения')
    
textResults=textProcessing.textProcessing(df,coursePortrait,textFields)

assessmentsPage.assessmentsGraphs(df,surveysCounter,coursePortrait,avgErr,textResults,textFields)




    
    
