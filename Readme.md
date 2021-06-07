Script to Download all the files from Google Drive

Pre-requisites :  

Set up the Oauth consent for the google drive to make API accessbile

Follow the below links to enable drive API and to Authenticate the user:

https://developers.google.com/drive/api/v3/enable-drive-api
https://developers.google.com/drive/api/v3/about-auth

Download the token as json file and keep it in the script folder with the name "credentials.json"

Script Trigger :

1. Open the command prompt 
2. Navigate to the script path
3. Run the script using command : python googledrive.py


 Function Level Description:
 
 generateToken : This function perform the authorization/authentication for the googleAPI.
				 For the first time of exectuion it will prompt the GUi interface and will expect from USer to allow the permissions needed.
				 It will save the tokens needed in tocken.pickle file and will use that in future.

 getFileList   : This function will fetch the list of all files present on the drive.
				 It will check the mimeType and will ignore the folder and put the rest in the list
				 Each object in the list will have id , name and mimetype

 downloadFiles : This function will download the files provide the fileId and FileName
				 Based on the filedId provided consturctor will be created and will be used to download the file first to RAM
				 From RAM it will be written to file with name provided to function
				 

