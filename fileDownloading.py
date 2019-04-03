#if you are running this project from collaboratory, you must download a file with surveys results
import os
import sys

def downloadingFromGoogleDrive(docId,isZip):
        if not (os.path.exists(os.getcwd()+'//surveys')
                or os.path.exists(os.getcwd()+'/surveys')):
            os.mkdir(surveys)
        os.chdir('surveys')
        
        try:
            from google_drive_downloader import GoogleDriveDownloader as gdd
        except ModuleNotFoundError:
            print('You must install google_drive_downloader: pip install googledrivedownloader')
            sys.exit
                
        gdd.download_file_from_google_drive(file_id=docId, 
                                            dest_path='surveys/surveys.csv',
                                            unzip=isZip)