import os
import pandas as pd
import numpy as np

import fileDownloading
from dataPreparation import dataPreparation
from calculations import assessmentsProcessing
from visualization import assessmentsPage

"""
!pip install dash-table
"""

try:
    import dash
except ModuleNotFoundError:
    !pip install dash
    import dash
    
try:
    import dash_core_components as dcc
except ModuleNotFoundError:
    !pip install dash-core-components
    import dash_core_components as dcc
    
try:
    import dash_html_components as html  
except ModuleNotFoundError:
    !pip install dash-html-components
    import dash_html_components as html  
    
#settings

isFileNeedToBeDownloaded=False 
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

df=dataPreparation.dataPreparation(df) #if a survey was changed this function need to be fixed

coursePortrait=assessmentsProcessing.assessmentsProcessing(df)

assessmentsPage.assessmentsGraphs(coursePortrait)


    
    
