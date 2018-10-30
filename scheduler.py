from multiprocessing import Process

from user.aid_mid import AidMid
from user.userinfo import UserInfo

from downloader.get_arcurl import GetAid
from downloader.get_video_address import GetVideoURL
from downloader.save_video import SaveVideo
from logs.log import Log


class Scheduler(object):
    @staticmethod
    def aid_mid():
        AidMid().run()

    @ staticmethod
    def user_info():
        UserInfo().run()

    @staticmethod
    def downloader():
        arcurl = GetAid().get_aid()
        get_video = GetVideoURL(arcurl)
        current_url, video_title, video_url_list = get_video.run()
        SaveVideo(current_url, video_title, video_url_list).run()

    def run(self):
        p1 = Process(target=self.aid_mid)
        p1.start()

        p2 = Process(target=self.user_info)
        p2.start()

        # p3 = Process(target=self.downloader)  #
        # p3.start()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
