import re
import time
import json

import urllib.request
from concurrent.futures import ThreadPoolExecutor

from database.db import MySQLDB
from utils.config import parse_url, SECONDS


class UserInfo(object):
    def __init__(self):
        self.mid_url = "https://api.bilibili.com/x/web-interface/card?mid={}"
        self.face_re = re.compile(r".*\/(.*?)\.(\w+)", re.S)

    def get_user_info(self, base_mid):
        """
        According to mid get user's information
        :return:
        """
        html = parse_url(self.mid_url.format(base_mid))
        if html is None:
            return
        # print(html)
        html = json.loads(html)
        fans = html["data"]["card"]["fans"]
        if fans < 100000:
            self.mark_mid(base_mid)
            print(f"----This mid ({base_mid}) user's fans too little----")
            time.sleep(SECONDS)
            return
        mid = html["data"]["card"]["mid"]
        name = html["data"]["card"]["name"]
        sex = html["data"]["card"]["sex"]
        face_url = html["data"]["card"]["face"]
        face = self.download_face(face_url)  # Download face image
        regtime = html["data"]["card"]["regtime"]
        sign = html["data"]["card"]["sign"]
        birthday = html["data"]["card"]["birthday"]
        place = html["data"]["card"]["place"]
        current_level = html["data"]["card"]["level_info"]["current_level"]
        friends = html["data"]["card"]["friend"]
        attention = html["data"]["card"]["attention"]
        archive_count = html["data"]["archive_count"]
        article_count = html["data"]["article_count"]
        user_info = (name, sex, face, regtime, sign, birthday, place, current_level, fans, friends, attention,
                     archive_count, article_count, mid)
        self.update_user_info(user_info)
        time.sleep(SECONDS)

    def update_user_info(self, user_info):
        """
        Update user's information to database
        :param user_info:
        :return:
        """
        user_sql = "UPDATE userinfo SET name=%s, sex=%s, face=%s, regtime=%s, sign=%s, birthday=%s, place=%s, current_level=%s, fans=%s, friends=%s, attention=%s, archive_count=%s, article_count=%s, mark=1 where mid=%s;"
        MySQLDB.update(user_sql, user_info)

    def mark_mid(self, base_mid):
        """
        Mark mid been used
        :param base_mid:
        :return:
        """
        mark_sql = f"UPDATE userinfo SET MARK=1 WHERE mid={base_mid}"
        MySQLDB.update(mark_sql)

    def download_face(self, face_url):
        """
        Download face image and save local path
        :param face_url:
        :return:
        """
        if face_url:
            face_content = self.face_re.findall(face_url)[0]
            face_code = face_content[0]
            face_name = ".".join(face_content)
            local_path = f"./face/{face_name}"
            try:
                # urllib.request.urlretrieve(face_url, local_path)  # If you want download face image, open the annotation
                return face_code
            except Exception as e:
                print(f"----Download face image failure {e}----")
                return "face download failure"

    def mid_select(self):
        """
        Select mid from database
        :return:
        """
        f = ThreadPoolExecutor(max_workers=1)
        offset = 0
        while True:
            mid_sql = f"select mid from userinfo where mark=0 limit {offset},10;"
            mids = MySQLDB.select(mid_sql)
            if mids is None:
                break
            for mid in mids:
                f.submit(self.get_user_info, mid[0].decode("utf-8"))
            offset += 10
            time.sleep(10)  # Based on the request frequency decide how many seconds to sleep

    def run(self):
        self.mid_select()


if __name__ == '__main__':
    user = UserInfo()
    while True:
        user.run()
        time.sleep(60*30)
