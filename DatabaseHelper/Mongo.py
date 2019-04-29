from pymongo import MongoClient
import pymongo


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

class Database(object):
    URI = "mongodb://localhost:27017"
    DATABASE = None


def initialise(object):
    client = pymongo.MongoClient(Database.URI)
    Database.DATABASE = client['publictv']


def insert(collection, data):
    # Database.DATABASE[collection].insert(data)
    Database.DATABASE[collection].update(
        {"VideoDeviceMapId": data['VideoDeviceMapId']},
        {"$set":
            {
                "VL_VideoID": data['VL_VideoID'],
                "VL_VideoName": data['VL_VideoName'],
                "VL_Size": data['VL_Size'],
                "VL_DriveFileId": data['VL_DriveFileId'],
                "VL_VideoType":data['VL_VideoType'],
                "VL_Description":data['VL_Description'],
                "VL_Status":data['VL_Status'],
                "VL_FileMimeType":data['VL_FileMimeType'],
                "VL_FileTags":data['VL_FileTags'],
                "VL_UploadedDate":data['VL_UploadedDate'],
                "VDL_Impressions":data['VDL_Impressions'],
                "VDL_TotalImpression": data['VDL_TotalImpression'],
                "VDL_EndDate":data['VDL_EndDate'],
                "CampaignId":data['CampaignId']
            }
        }, upsert=True
    )


def findall(collection, query):
    return Database.DATABASE[collection].find()
