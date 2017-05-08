#!/usr/bin/env python 
#coding=utf-8
#
import requests
from bs4 import BeautifulSoup
#
import user_agent


class LiaoXueFeng():
    def get_GIT(self):
        url = 'http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000'
        headers = user_agent.get_headers()
        resp = requests.get(url, headers=headers, timeout=5)
        resp.encoding = 'bgk'
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        #print(soup.prettify())
        content = soup.prettify().encode(encoding="utf-8")
        self.save('xx.html', content)
        pass

    def save(self, filename, contents):
        fh = open(filename, 'wb')
        fh.write(contents)
        fh.close()

    pass


if '__main__' == __name__:
    obj = LiaoXueFeng()
    obj.get_GIT()