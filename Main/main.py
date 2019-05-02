from Advertisement import PlayAdvts
from DatabaseHelper import Mongo
from Main import DownloadVideos
from Models import Model
from Extras import CommonDataArea

def main():
    m = Mongo.Database()
    m.initialise()
    advts=Model.post()
    advts.start()

    print("python main function")
    # obj = PlayAdvts.Advt_player()
    # obj.daily_playcount_updater()



if __name__ == '__main__':
    main()







# obj.select_videos_to_play()





#
# # #Model.json_data()
# # m=Model.post()
# # m.save_to_video_collection()
#
#
# #Model.videos('473')
# # file_id = '1LDEAnM-zRF1h-B5R4qHed5honEQEaF81'
# # destination = 'F:/ptv_videos/terrace latest_1553062496.mp4'
# # DownloadVideos.download_file_from_google_drive(file_id, destination)
# p=PlayAdvts
# path = 'F:/ptv_videos/'
# files=os.listdir(path)
# for f in files:
#     print(f)
#     videopath=path+f
#     p.play_videos(videopath)

#data=m.Advertisement_selector("Advertisement_List")
# data=spli
# m=Model.post()
# m.save_to_video_collection()

# a=PlayAdvts.Advt_player()
# a.Daily_Advt_play_count()