import io
import logging
from datetime import datetime
import sys
import pickle
import os.path
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import DefaultCredentialsError

global resource
creds = None
fetchfile_iteration = 0
listofFiles = []
SCOPES = ['https://www.googleapis.com/auth/drive']

now = datetime.now()
logging.basicConfig(
   level=logging.DEBUG,
   format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s',
   filename="LogFile-" + str(now.strftime("%H-%M-%S")) + ".log",
   filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def generateToken():
	logging.info("Running generateToken to do authentication and Authorization")
	global creds
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

def getFileList(nextPageToken=None):
	global fetchfile_iteration
	fetchfile_iteration += 1
	logging.info("Running getFileList to get list of files -- Iteration : " + str(fetchfile_iteration))
	try:
		result = resource.list(pageToken=nextPageToken, fields="nextPageToken, files(id, name, mimeType)").execute()
	except Exception as error:
		logging.error("Listing of Files failed with error : " + str(error))
		sys.exit(1)
	file_list = result.get('files')
	for file in file_list:
		if "folder" not in file['mimeType']:
			listofFiles.append(file)
	return result

def downloadFiles(FileId,FileName):
	logging.info("Running downloadFiles to download file : " + FileName)
	request = resource.get_media(fileId=FileId)
	fh = io.BytesIO()
	downloader = MediaIoBaseDownload(fh, request)
	download_done = False
	while download_done is False:
		try:
			status, download_done = downloader.next_chunk()
			logging.info("Downloading %s in Progress" %(FileName))
		except Exception as error:
			logging.error("Download of File failed with the error :" +  str(error))
			sys.exit(1)
	fh.seek(0)
	try:
		with open(FileName, 'wb') as f:
			shutil.copyfileobj(fh, f, length=131072)
	except Exception as error :
		logging.error("Copying content of file to disk Failed with error : " + str(error))
		sys.exit(1)

if __name__ == "__main__":
	try:
		generateToken()
	except TimeoutError as err:
		print("Error Happened because of timeout")
		sys.exit(1)
	except DefaultCredentialsError as err:
		print("Error happened because of Access Denied")
		sys.exit(1)
	except Exception as err:
		("Failed to generate auth token")
		sys.exit(1)
	service = build('drive', 'v3', credentials=creds)
	resource = service.files()
	result_dict = getFileList()
	while 'nextPageToken' in result_dict.keys():
		nextPageToken = result_dict['nextPageToken']
		result_dict = getFileList(nextPageToken)
	path = os.path.dirname(os.path.realpath(__file__)) + "\\googlefiles\\"
	if not os.path.isdir(path):
		os.mkdir(path)
	for file in listofFiles:
		downloadFiles(file['id'],path + file['name'])
	logging.info("Download Completed")