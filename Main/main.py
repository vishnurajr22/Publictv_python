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
    obj = PlayAdvts.Advt_player()
    obj.daily_playcount_updater()



if __name__ == '__main__':
    main()