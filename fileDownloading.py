#if you are running this project from collaboratory, you must download a file with surveys results
def downloadingFromGoogleDrive(docId,isZip):
        if not (os.path.exists(os.getcwd()+'//surveys')
                or os.path.exists(os.getcwd()+'/surveys')):
            os.mkdir(surveys)
        os.chdir('surveys')
        
        try:
            from google_drive_downloader import GoogleDriveDownloader as gdd
        except ModuleNotFoundError:
            !pip install googledrivedownloader
            from google_drive_downloader import GoogleDriveDownloader as gdd
                
        gdd.download_file_from_google_drive(file_id=docId, 
                                            dest_path='surveys/surveys.csv',
                                            unzip=isZip)