import os
import sys
import pandas as pd
import zipfile

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
    print('You must get file with surveys results to \'surveys\' folder')
else:
    os.chdir('surveys')
    
filename=-1
files=os.listdir()
for file in files:
    if str(file).find('.csv')!=-1:
        filename=file
        break
if filename==-1:
    print('You must get file with surveys results to \'surveys\' folder')
    sys.exit()
    
df = pd.read_csv(filename, sep=',', encoding='utf-8', 
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




    
    
