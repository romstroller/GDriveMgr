import os 
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

""" FIRST:
    Get Authentication for Google Service API 
    https://pythonhosted.org/PyDrive/quickstart.html
    https://cloud.google.com/docs/authentication

    requires local exposure of secrets json; move to eg. keyring-based auth
        see: https://pythonhosted.org/PyDrive/oauth.html
"""

class GDriveHandler():
    
    def __init__(self, uplLocPath ):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)

    def listDriveDir( self,):
        # list files at Drive location
        return { li_file['id'] : li_file['title'] for li_file in 
            self.drive.ListFile({'q': "'root' in parents and trashed=false"}
            ).GetList() }

    def setUploads( self, local_upDir ):
        # DICT: set files ( name, path ) for upload
        self.filesUp_dct = { 
            fName : os.path.abspath( f'{local_upDir}/{fName}' ) 
            for fName in os.listdir( local_upDir ) }
        return self.filesUp_dct

    def testUploaded( self ):
        # test if files at Drive location:
        testUpl = { f : ( f in listDriveDir().values() ) 
            for f in self.filesUp_dct.keys() }
        print( "In drive:\n" )
        for file, found in testUpl.items(): print( f"{file}: {found}" )
        return testUpl

    def uploadFiles( self ):
        # Upload to drive
        for fName_up, fPath_up in self.filesUp_dct.items():
            gFile = self.drive.CreateFile( { 'title': fName_up, } )
            gFile.SetContentFile( fPath_up )
            gFile.Upload()
            