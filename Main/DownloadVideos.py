import requests
import os.path
from os import path
import threading
filepath='F:/ptv_videos/'
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    print(response)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    print('download success')
def get_size(start_path):
    b = os.path.getsize(start_path)
    return b



def check_videos_existing_or_not(post):
        print(filepath+str(post.VL_DriveFileId+'.'+post.VL_FileMimeType))
        print ("file exist:"+str(path.exists(filepath+str(post.VL_DriveFileId+'.'+post.VL_FileMimeType))))
        print(str(post.VL_DriveFileId+'.'+post.VL_FileMimeType))
        if (path.exists(filepath+str(post.VL_DriveFileId+'.'+post.VL_FileMimeType))):
            size=str (get_size(filepath+str(post.VL_DriveFileId+'.'+post.VL_FileMimeType)))
            if size == post.VL_Size:
                print('size equal')
            else:
                print('size not equal')
                os.remove(filepath+str(post.VL_DriveFileId+'.'+post.VL_FileMimeType))
                print(os)
        else:
            t1 = threading.Thread(target=download_file_from_google_drive, args=(post.VL_DriveFileId,filepath+post.VL_DriveFileId+'.'+post.VL_FileMimeType,))
            #download_file_from_google_drive(post.VL_DriveFileId,filepath+post.VL_DriveFileId+'.'+post.VL_FileMimeType)
            t1.start()
            t1.join()