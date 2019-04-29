import uuid
from Main import DownloadVideos
from DatabaseHelper import Mongo
import requests
import  json

class post(object):
    def __init__(self, id=None,VideoDeviceMapId=None,VL_VideoID=None,VL_VideoName=None,
                 VL_Size=None,VL_DriveFileId=None ,VL_VideoType=None,VL_Description=None,
                 VL_Status=None,VL_FileMimeType=None,VL_FileTags=None,
                 VL_UploadedDate=None,VDL_Impressions=None,VDL_TotalImpression=None,
                 VDL_EndDate=None,CampaignId=None):

            self.ids = id

            self.VideoDeviceMapId=VideoDeviceMapId
            self.VL_VideoID=VL_VideoID
            self.VL_VideoName=VL_VideoName
            self.VL_Size=VL_Size
            self.VL_DriveFileId=VL_DriveFileId
            self.VL_VideoType=VL_VideoType
            self.VL_Description=VL_Description
            self.VL_Status=VL_Status
            self.VL_FileMimeType=VL_FileMimeType
            self.VL_FileTags=VL_FileTags
            self.VL_UploadedDate=VL_UploadedDate
            self.VDL_Impressions=VDL_Impressions
            self.VDL_TotalImpression=VDL_TotalImpression
            self.VDL_EndDate=VDL_EndDate
            self.CampaignId=CampaignId



    def setid(self,id):
            self.ids=id
    def getid(self=None):
            return self.ids

    @staticmethod
    def save_to_video_collection():

            data=post.get_video_api()
            pdata=json.loads(data.text)
            for d in pdata:
                p=post()
                p.ids=uuid.uuid4()
                p.VideoDeviceMapId=d['VideoDeviceMapId']
                p.VL_VideoID=d['VL_VideoID']
                p.VL_VideoName=d['VL_VideoName']
                p.VL_Size=d['VL_Size']
                p.VL_DriveFileId=d['VL_DriveFileId']
                p.VL_VideoType=d['VL_VideoType']
                p.VL_Description=d['VL_Description']
                p.VL_DriveFileId=d['VL_DriveFileId']
                p.VL_Status=d['VL_Status']
                p.VL_FileMimeType=d['VL_FileMimeType']
                p.VL_FileTags=d['VL_FileTags']
                p.VL_UploadedDate=d['VL_UploadedDate']
                p.VDL_Impressions=d['VDL_Impressions']
                p.VDL_TotalImpression=d['VDL_TotalImpression']
                p.VDL_EndDate=d['VDL_EndDate']
                p.CampaignId=d['CampaignId']

                down=DownloadVideos
                down.check_videos_existing_or_not(p)
                #print(p.VL_DriveFileId)
                #Mongo.insert(collection='video',data=d)



    @staticmethod
    def get_video_api():
                response = requests.get('http://publictvads.in/WebServiceLiveTest/GetVideoList.php?id=3caa0fb698c0a234',
                                        auth=('user', 'password'))
                data = response.json()
               # print(data)
                return response

    def videos(id):
            data=Mongo.findall(collection='video',query={'VL_VideoID':id})
            for data in data:

                print(data["VL_FileTags"])

