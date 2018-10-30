import os
import re

import requests

from utils.config import HEADERS


class SaveVideo(object):
    def __init__(self, current_url, video_title, video_url_list):
        self.headers = HEADERS
        self.headers["Host"] = re.findall(r".*?\/\/(.*?)\/", video_url_list[0])[0]
        self.headers["Referer"] = current_url
        self.title = video_title
        self.video_url_list = video_url_list[0]
    
    def downloader(self):
        """
        According to the video URL, download video and save local path
        :return:
        """
        try:
            local_path = f"./bilibili/video/{self.title}.mp4"
            pre_content_length = 0
            # Cycle receive video data
            while True:
                # If file exist, continue and set the local path for receive data
                if os.path.exists(local_path):
                    self.headers['Range'] = 'bytes=%d-' % os.path.getsize(local_path)

                res = requests.get(self.video_url_list, stream=True, headers=self.headers, verify=False)
                print(res.status_code)

                content_length = int(res.headers['Content-Length'])
                # If the current message length is less than the previous message length,
                # or the received file is equal to the current message length, video reception can be considered complete
                if content_length < pre_content_length or (
                        os.path.exists(local_path) and os.path.getsize(local_path) == content_length):
                    break
                pre_content_length = content_length

                # Write the receive video data to local path
                with open(local_path, 'ab') as file:
                    file.write(res.content)
                    file.flush()
                    print('receive data，file size : %d   total size:%d' % (os.path.getsize(local_path), content_length))
        except Exception as e:
            print(e)

    def run(self):
        self.downloader()


