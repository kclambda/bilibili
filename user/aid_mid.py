import re
import time

from concurrent.futures import ThreadPoolExecutor

from database.db import MySQLDB
from utils.config import parse_url, SECONDS


class AidMid(object):
    def __init__(self):
        self.base_url = "https://api.bilibili.com/x/web-interface/view/detail?jsonp=jsonp&aid={}"
        self.mid_url = "https://api.bilibili.com/x/web-interface/card?mid={}"
        self.re_mid = re.compile(r'"mid":(\d+)', re.S)
        self.re_aid = re.compile(r'"aid":(\d+)', re.S)

    def get_html(self, aid):
        """
        Get html page source
        :return: 
        """
        url = self.base_url.format(aid)
        html = parse_url(url)
        # print(html)
        if html is None:
            exit()  # That's not good
        self.get_mid_aid(html, aid)

    def get_mid_aid(self, html, base_aid):
        """
        By any video url get mid and aid
        :return:
        """
        mid_list = self.re_mid.findall(html)
        self.insert_mid(mid_list)

        aid_list = self.re_aid.findall(html)
        self.aid_insert(aid_list, base_aid)

    @staticmethod
    def insert_mid(mid_list):
        """
        Save user's mid to userinfo table
        :return:
        """
        user_sql = "insert into userinfo(mid) values({});"
        MySQLDB.insert_many(user_sql, mid_list)

    @staticmethod
    def aid_insert(aids, base_aid):
        """
        Insert video's aid to aid table and mark the aid been used
        :return:
        """
        aid_sql = "INSERT INTO aid(aid) VALUES ({});"
        MySQLDB.insert_many(aid_sql, aids)

        mark_sql = "UPDATE aid SET mark=1 where aid={};".format(base_aid)
        MySQLDB.update(mark_sql)

    def aid_select(self):
        """
        Select aid from database
        :return:
        """
        f = ThreadPoolExecutor(max_workers=3)
        offset = 0
        while True:
            aid_sql = f" select aid from aid where mark=0 limit {offset},10;"
            aids = MySQLDB.select(aid_sql)
            if aids is None:
                break
            for base_aid in aids:
                f.submit(self.get_html, base_aid[0].decode("utf-8"))
                time.sleep(SECONDS)
            offset += 10
            time.sleep(10)  # This is not necessary, depend on the real situation

    def run(self):
        self.aid_select()


if __name__ == '__main__':
    aid_mid = AidMid()
    aid_mid.run()

