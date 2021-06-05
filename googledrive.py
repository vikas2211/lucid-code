# import the required libraries
import io
import pickle
import os.path
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



# Define the SCOPES. If modifying it,
# delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/drive']



# Create a function getFileList with
# parameter N which is the length of
# the list of files.
def getFileList(nextPageToken=None):

	# Variable creds will store the user access token.
	# If no valid token found, we will create one.
	creds = None

	# The file token.pickle stores the
	# user's access and refresh tokens. It is
	# created automatically when the authorization
	# flow completes for the first time.

	# Check if file token.pickle exists
	if os.path.exists('token.pickle'):

		# Read the token from the file and
		# store it in the variable creds
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	# If no valid credentials are available,
	# request the user to log in.
	if not creds or not creds.valid:

		# If token is expired, it will be refreshed,
		# else, we will request a new one.
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)

		# Save the access token in token.pickle
		# file for future usage
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	# Connect to the API service
	service = build('drive', 'v3', credentials=creds)

	# request a list of first N files or
	# folders with name and id from the API.
	resource = service.files()
	result = resource.list(pageToken=nextPageToken, fields="nextPageToken, files(id, name, mimeType)").execute()
	file_id = '1Yx3rIa7fCvu_3AFpOHQhzjUpDfNWMA2D'
	request = resource.get_media(fileId=file_id)
	#destinationfile = 'vikdocument'
	fh = io.BytesIO()
	downloader = MediaIoBaseDownload(fh, request)
	done = False
	while done is False:
		status, done = downloader.next_chunk()
		print("Download in Progress")
        #print("Download %d%%." % int(status.progress() * 100))
	fh.seek(0)
	with open('your_filename', 'wb') as f:
		shutil.copyfileobj(fh, f, length=131072)
	#return the result dictionary containing
	#the information about the files
	return result


	
# Get list of first 5 files or
# folders from our Google Drive Storage
result_dict = getFileList()
'''while 'nextPageToken' in result_dict.keys():
    nextPageToken = result_dict['nextPageToken']
    result_dict = getFileList(nextPageToken)
'''
# Extract the list from the dictionary
file_list = result_dict.get('files')
fileId = file_list[0]["id"]
print(fileId)
#for item in file_list:
 #   print(item)
  #  if "Cool" in item['name']:
   #     print("Found")
    #    print(item)
    #else:
     #   print("Not FOund")
# Print every file's name
#for file in file_list:
    #print(file['name']