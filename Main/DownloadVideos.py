import requests
import os.path
from os import path
import threading
from DatabaseHelper import Mongo
from Extras import CommonDataArea
filepath='F:/ptv_videos/'
is_downloaded=False
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
    globals()['is_downloaded']=True

def get_size_of_file_in_storage(start_path):
    b = os.path.getsize(start_path)
    return b



def check_videos_existing_or_not(model):
        db=Mongo.Database()

        '''print(filepath + str(model.VL_DriveFileId + '.' + model.VL_FileMimeType))
        #print ("file exist:" + str(path.exists(filepath + str(model.VL_DriveFileId + '.' + model.VL_FileMimeType))))
        print(str(model.VL_DriveFileId + '.' + model.VL_FileMimeType))'''
        if (path.exists(filepath+str(model.VL_DriveFileId + '.' + model.VL_FileMimeType))):
            size=str (get_size_of_file_in_storage(filepath + str(model.VL_DriveFileId + '.' + model.VL_FileMimeType)))
            if size == model.VL_Size:
                print('size equal')
                if db.check_for_same_mapid(model.VideoDeviceMapId):
                    print(db.check_for_same_mapid(model.VideoDeviceMapId))
                    add_camp_to_Advertisement_List(model)
            else:
                print('size not equal')

                os.remove(filepath + str(model.VL_DriveFileId + '.' + model.VL_FileMimeType))
                download_file_from_google_drive(model.VL_DriveFileId,
                                                filepath + model.VL_DriveFileId + '.' + model.VL_FileMimeType)
                # t2=threading.Thread(target=download_file_from_google_drive, args=(model.VL_DriveFileId, filepath + model.VL_DriveFileId + '.' + model.VL_FileMimeType,))
                # t2.start()
                # t2.join()
                if is_downloaded:
                    if db.check_for_same_mapid(model.VideoDeviceMapId):
                        print(db.check_for_same_mapid(model.VideoDeviceMapId))
                        add_camp_to_Advertisement_List(model)

        else:
            #t1 = threading.Thread(target=download_file_from_google_drive, args=(model.VL_DriveFileId, filepath + model.VL_DriveFileId + '.' + model.VL_FileMimeType,))
            download_file_from_google_drive(model.VL_DriveFileId,filepath+model.VL_DriveFileId+'.'+model.VL_FileMimeType)
            # t1.start()
            # t1.join()
            print(is_downloaded)
            if is_downloaded:
                if db.check_for_same_mapid(model.VideoDeviceMapId):
                    print(db.check_for_same_mapid(model.VideoDeviceMapId))
                    add_camp_to_Advertisement_List(model)

def add_camp_to_Advertisement_List(model):
    mongo=Mongo.Database()
    date=CommonDataArea.CommonDataArea.curent_time()
    # if model["video_status"]==date:
    try:
        mongo.insert_to_Advertisement_List(collection='Advertisement_List',data=model)
    except Exception as e:
        print(e)


