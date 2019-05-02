from pymongo import MongoClient
import pymongo
from Extras import CommonDataArea

# client =MongoClient('localhost',8080)
# # print(client)
# db=client.test_database #or  db=client['test_database']>> object or array
# # print(db)
# cources=db.cources
# # print(cources)
# 
# course={
#     'author':'vishnu',
#     'course':"mongodb",
#     'price':100,
#     'rating':5
# }
# result=cources.insert_one(course)
# print(result)
from Models import Model


class Database(object):
    URI = "mongodb://localhost:27017"
    DATABASE = None


    def initialise(object):
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['publictv']

    @staticmethod
    def insert_to_Advertisement_List(collection, data):
        # Database.DATABASE[collection].insert(data)
        Database.DATABASE[collection].update(
            {"VideoDeviceMapId": data.VideoDeviceMapId},
            {"$set":
                {

                    "VL_VideoID": data.VL_VideoID,
                    "VL_VideoName": data.VL_VideoName,
                    "VL_Size": data.VL_Size,
                    "VL_DriveFileId": data.VL_DriveFileId,
                    "VL_VideoType":data.VL_VideoType,
                    "VL_Description":data.VL_Description,
                    "VL_Status":data.VL_Status,
                    "VL_FileMimeType":data.VL_FileMimeType,
                    "VL_FileTags":data.VL_FileTags,
                    "VL_UploadedDate":data.VL_UploadedDate,
                    "VDL_Impressions":data.VDL_Impressions,
                    "VDL_TotalImpression": data.VDL_TotalImpression,
                    "VDL_EndDate":data.VDL_EndDate,
                    "CampaignId":data.CampaignId,
                    "video_status":data.video_status
                }
            }, upsert=True
        )


    def findall(collection, query):
        return Database.DATABASE[collection].find()
    @staticmethod
    def random_5(no_of_videos_to_be_played):
        cda=CommonDataArea.CommonDataArea()
        date=cda.curent_time()
        nn = Database.DATABASE['Advertisement_List'].aggregate([
        {'$match': {"video_status": date,'VDL_Impressions': {'$ne':"0"}}},
        {'$sample': {'size': no_of_videos_to_be_played}}
        ])
        return nn
    @staticmethod
    def Advertisement_selector(collection):

        data=Database.DATABASE[collection].find(
             # {"video_status":"0"}
        )
        # for d in data:
        return data


    @staticmethod
    def update_video_status_for_daily_play_count(mapid,status,daily_imp):
        Database.DATABASE["Advertisement_List"].update_one({
            'VideoDeviceMapId': mapid
        }, {
            '$set': {
                'video_status': status,
                'VDL_Impressions':daily_imp
            }
        }, upsert=False)

    @staticmethod
    def update_play_count(mapid,daily_imp,total_imp):
        Database.DATABASE["Advertisement_List"].update(
            {
                'VideoDeviceMapId': mapid
            },{
                '$set': {
                    'VDL_Impressions': str(daily_imp),
                    'VDL_TotalImpression': str(total_imp)
                }
            },upsert=True
        )

    @staticmethod
    def playtime_data(mapid,total_imp,daily_imp,CampaignId,VideoName,VideoDescription,DriveId,VideoExtension,EndDate):
            obj = CommonDataArea.CommonDataArea()
            time = obj.date_with_time()
            Database.DATABASE["PlayTimeList"].insert([
                {'MapId':mapid,'CampaignId':CampaignId,'VideoName':VideoName,
                 'PlayedTime':time,'RemainingTotalImpression':str(total_imp),
                 'RemainingDailyImpression':str(daily_imp),'VideoDescription':VideoDescription,
                 'DriveId':DriveId,'VideoExtension':VideoExtension,
                 'EndDate':EndDate}]

            )















    # def random_5(no_of_videos_to_be_played):
    #     cda=CommonDataArea.CommonDataArea()
    #     date=cda.curent_time()
    #     nn = Database.DATABASE['Advertisement_List'].aggregate([
    #     {'$match': {"video_status" : date}},
    #     {'$sample': {'size': no_of_videos_to_be_played}}
    #     ]);
    #     return nn


