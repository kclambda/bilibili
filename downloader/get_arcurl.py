from database.db import MySQLDB


class GetAid(object):
    def __init__(self):
        self.base_url = "https://www.bilibili.com/video/av{}/"

    def get_aid(self):
        """
        Get video's aid from database
        :return:
        """
        aid_sql = "SELECT aid FROM aid limit 0, 1;"
        aid = MySQLDB.select(aid_sql)
        if aid is None:
            return
        url = self.base_url.format(aid[0][0].decode("utf-8"))
        return url


if __name__ == '__main__':
    aid = GetAid()
    url = aid.get_aid()
    if url is not None:
        print(url)