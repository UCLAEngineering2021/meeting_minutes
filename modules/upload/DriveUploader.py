#imports
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#DriveUploader
#
#Instance Data
# authorized: boolean are we authorized by OAUTH 2.0, and by the user to perform an
#              upload onto google drive
#
# uploading: boolean are we currently uploading the MeetingDocument onto google drive

#Static Const Data
# HOME_DIR: Stores the home directory for the filesysem
#
# UPLOAD_SCOPE: Stores the scope of access google's user is granting us.
#               For write access, we need: https://www.googleapis.com/auth/drive
#
# SECRET_CLIENT_NAME: Stores the file name of the client json file storing settings and configurations for
#                     authorization to access the user's google drive
#
# AUTH_DIRECTORY_PATH: Path to the directory where the client json file is stored
#
# APPLICATION_NAME: Name of this application. 'Clubby'
#
# DOCX_MIME_TYPE: Mime type used to upload.  application/vnd.openxmlformats-officedocument.wordprocessingml.document
#
# GOOGLE_DOC_MIME_TYPE: Mime type to convert to. application/vnd.google-apps.document.

HOME_DIR = '~'
UPLOAD_SCOPE = 'https://www.googleapis.com/auth/drive'
SECRET_CLIENT_NAME = 'client_secrets.json'
AUTH_DIRECTORY_PATH = '/Desktop/meeting_minutes/auth/'
APPLICATION_NAME = 'Drive API Meeting Minutes'
DOCX_MIME_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
GOOGLE_DOC_MIME_TYPE = 'application/vnd.google-apps.document.'


class DriveUploader:


    #Methods

    # initialize critical member variables
    def __init__(self):
        self.authorized = False
        self.uploading = False

    # upload the full contents of the MeetingDocument onto the user's google drive
    def upload(self, doc):
        # if not uploading already
        if(not self.uploading):
            # set uploading member variable to true
            self.uploading = True
            # authorize the upload
            http = self._authorize()
            # set metadata
            # set metadata-name
            # set metadata-mime-type
            doc_metadata = {'name' : doc.getName(),
                            'mimeType' : DOCX_MIME_TYPE}
            # for this upload, I used a simple media upload because of the relative small size of the meeting documents and the
            # ease of media upload
            # initialize the media file upload
            media = MediaFileUpload(doc.getPath(),
                                    mimetype=GOOGLE_DOC_MIME_TYPE,
                                    resumable=True)
            # build a google drive service object
            drive_service = discovery.build('drive', 'v3', http=http)
            # initialize a google file object in google drive
            google_file = drive_service.files().create(body=doc_metadata,
                                                       media_body=media,
                                                       fields='id').execute()
            self.uploading = False

    #Private Methods

    #receive authorization to upload document
    #returns google's http object for use building a drive service object
    def _authorize(self):
        # retrieve the relevant user credentials
        credentials = self._getCredentials()
        # authorize uploading from credentials
        http = credentials.authorize(httplib2.Http())
        # set authorized member variable to reflect authorization
        self.authorized = True
        print('Authorization Successful.')
        return http

    #retrieve the user's stored credentials.
    #flow refers to the authorization process
    """Gets valid user credentials from storage.

            If nothing has been stored, or if the stored credentials are invalid,
            the OAuth2 flow is completed to obtain the new credentials.

            Returns:
            Credentials, the obtained credential.
    """
    def _getCredentials(self):
        # get the path to the home directory
        home_dir = os.path.expanduser(HOME_DIR)
        # get the path to the directory containing the credentials
        credential_dir = os.path.join(home_dir, '.credentials')
        credential_path = os.path.join(credential_dir, 'meeting_minutes_api_credentials.json')
        # if the cred folder doesn't exist, create it
        if not os.path.exists(credential_dir):
            print('Making credential dir')
            os.makedirs(credential_dir)
        # now retrieve the credentials from Google's storage
        store = Storage(credential_path)
        credentials = store.get()
        # if the credentials don't exist or are invalid
        if not credentials or credentials.invalid:
            # initiate the authorization process
            flow = client.flow_from_clientsecrets(home_dir + AUTH_DIRECTORY_PATH + SECRET_CLIENT_NAME, UPLOAD_SCOPE)
            # set the application requesting access to user data as the application name
            flow.user_agent = APPLICATION_NAME
            flags=tools.argparser.parse_args(args=[])
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        #return the authorized credentials
        return credentials

    #returns true if the application is authorized to proceed with the file upload
    def _isAuthorized(self):
        return self.authorized
