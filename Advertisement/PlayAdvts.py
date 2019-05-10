import cv2
import numpy as np
from Extras import CommonDataArea
from DatabaseHelper import Mongo
import tkinter as tk
from os.path import isfile, join
import time
from datetime import date
from datetime import datetime

from Models import Model


class Advt_player:
    status = None

    @staticmethod
    def play_videos(video):
        videoPath = 'F:/ptv_videos/' + video
        cap = cv2.VideoCapture(videoPath)
        x = tk.Tk()
        wd = x.winfo_screenmmwidth()
        ht = x.winfo_screenheight()
        print(ht)
        print(wd)

        while True:
            ret, frame = cap.read()
            if ret == True:

                ims = cv2.resize(frame, (ht, wd))
                cv2.imshow('frame', ims)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        return True

    @staticmethod
    def select_videos_to_play():
        rand = Mongo.Database()
        video_details = rand.random_5(CommonDataArea.CommonDataArea().no_of_videos)
        for f in video_details:
            video_name = f['VL_DriveFileId'] + '.' + f['VL_FileMimeType']
            daily_play_count = int(f['VDL_Impressions'])
            total_imp = int(f['VDL_TotalImpression'])
            mapid = f['VideoDeviceMapId']
            CampaignId = f["CampaignId"]
            VDL_EndDate = f["VDL_EndDate"]
            VL_Description = f["VL_Description"]
            VL_DriveFileId = f["VL_DriveFileId"]
            VL_FileMimeType = f["VL_FileMimeType"]
            VL_FileTags = f["VL_FileTags"]
            VL_Size = f["VL_Size"]
            VL_Status = f["VL_Status"]
            VL_UploadedDate = f["VL_UploadedDate"]
            VL_VideoID = f["VL_VideoID"]
            VL_VideoName = f["VL_VideoName"]

            detailslist = [CampaignId, VDL_EndDate, VL_Description, VL_DriveFileId, VL_FileMimeType, VL_FileTags,
                           VL_Size, VL_UploadedDate, VL_VideoID, VL_VideoName, ]
            play_obj = Advt_player()
            if daily_play_count != 0:
                sta = play_obj.play_videos(video_name)
                if sta:
                    rand.update_play_count(mapid=mapid, daily_imp=daily_play_count - 1, total_imp=total_imp - 1)
                    # Mongo.Database().playtime_data(mapid=mapid,total_imp=total_imp,daily_imp=daily_play_count,data=detailslist)
                    rand.playtime_data(mapid=mapid, total_imp=total_imp, daily_imp=daily_play_count,
                                       CampaignId=CampaignId, VideoName=VL_VideoName,
                                       VideoDescription=VL_Description, DriveId=VL_DriveFileId,
                                       VideoExtension=VL_FileMimeType,
                                       EndDate=VDL_EndDate)
            else:
                print("no videos to play")
            time.sleep(1)

    @staticmethod
    def daily_playcount_updater():

        objs = Mongo.Database()
        data = objs.Advertisement_selector("Advertisement_List")

        obj = CommonDataArea.CommonDataArea()
        status = str(obj.curent_time())
        for d in data:

            End_date = d["VDL_EndDate"]
            Total_imp = int(d['VDL_TotalImpression'])
            video_status = d['video_status']
            # print(End_date)

            dateTime1 = datetime.strptime(End_date, "%Y-%m-%d")

            if dateTime1.date() >= date.today():
                if video_status != status:
                    print("initialising daily play count")

                    date_format = "%Y-%m-%d"
                    today_date = datetime.strptime(status, date_format)
                    eending_date = datetime.strptime(End_date, date_format)
                    delta = eending_date - today_date
                    print(delta.days)
                    remaining_days = delta.days

                    global daily_impression

                    if remaining_days > 0:

                        daily_impression = Total_imp // remaining_days

                    else:
                        daily_impression = Total_imp

                    objs.update_video_status_for_daily_play_count(d['VideoDeviceMapId'], status, daily_impression)
                    print('updated video status')



            else:
                print("End date expired")
                continue
        selector = Advt_player()
        selector.select_videos_to_play()
        idle=CommonDataArea.CommonDataArea().idleTime
        time.sleep(idle)
        while True:
            Advt_player().daily_playcount_updater()