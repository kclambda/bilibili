import re
import time
import json

import requests

from utils.config import HEADERS, SECONDS


class GetVideoURL(object):
    def __init__(self, url):
        """
        Initialize regex
        :param url:
        """
        self.url = url

        self.videoTitle_re = re.compile(r"window.__INITIAL_STATE__=(.*?});", re.S)
        self.videoQuality_re = re.compile(r"window.__playinfo__=(.*?)</script>", re.S)

        # The filename cannot contain the following characters
        self.re_str = re.compile(r"\<|\>|\\|\*|\?|\:|\"|\/|\|", re.S)

    def get_html_source(self):
        """
        Get html source
        :return:
        """
        try:
            response = requests.get(self.url, headers=HEADERS)
            print(f"----Response status code {response.status_code}----")
            if response.status_code == 200:
                time.sleep(SECONDS)
                html = response.content.decode("utf-8")
                current_url = response.url
                return html, current_url
        except Exception as e:
            print(f"----Get page_source failure {e}----")

    def get_video_title(self, html):
        """
        Get video title
        :return:
        """
        try:
            title_text = self.videoTitle_re.findall(html)[0]
            title = json.loads(title_text)["videoData"]["title"]
            title = self.re_str.sub("", title)
            return title
        except Exception as e:
            print(f"----Get video title failure {e}----")

    def get_video_url(self, html):   
        """
        Get video download address
        :return: 
        """
        quality_text = self.videoQuality_re.findall(html)[0]
        json_str = json.loads(quality_text)
        """
        # There may be a variety of video formats, but we'll choose one by default
        video_quality = json_str["accept_description"]  # This video has clarity
        video_number = 1  # This video quality default 1080P
        quality_number = json_str['accept_quality'][video_number]  # This video clarity for quality number
        """
        video_url_list = json_str["durl"][0]['backup_url']
        video_url_list.insert(0, json_str["durl"][0]['url'])

        return video_url_list

    def run(self):
        html_source, current_url = self.get_html_source()
        if html_source is not None:
            video_title = self.get_video_title(html_source)
            video_url_list = self.get_video_url(html_source)

            return current_url, video_title, video_url_list


# if __name__ == '__main__':
#     videoUrl = GetVideoURL("https://www.bilibili.com/video/av34178809/")
#     current_url, video_title, video_url_list = videoUrl.run()
#     print(current_url, video_title, video_url_list)
#
