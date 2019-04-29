from DatabaseHelper import Mongo
from Models import Model
from Main import DownloadVideos
Mongo.initialise(object)

#Model.json_data()
m=Model.post()
m.save_to_video_collection()


#Model.videos('473')
# file_id = '1LDEAnM-zRF1h-B5R4qHed5honEQEaF81'
# destination = 'F:/ptv_videos/terrace latest_1553062496.mp4'
# DownloadVideos.download_file_from_google_drive(file_id, destination)

