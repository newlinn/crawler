#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
import requests
from bs4 import BeautifulSoup
import time
import json
import random
from csv_file import CsvFile
#
from proxy_pool import ProxyPool
import user_agent


class House:
    # 标签
    title = ''
    # 小区
    community = ''
    # 户型
    model = ''
    # 面积
    area = ''
    # 朝向
    direction = ''
    # 装修
    decoration = ''
    # 关注人数
    focus_num = ''
    # 观看人数
    watch_num = ''
    # 发布时间
    time = ''
    # 价格
    price = ''
    # 均价
    average_price = ''
    # 详情链接
    link = ''
    pass


class LianJia:

    def __init__(self):
        self._proxy_pool = ProxyPool()
        pass

    _proxy_pool = ''
    _timeout = 5
    _url = 'https://bj.lianjia.com/'
    _csv_file = CsvFile()
    _csv_rows = []

    def _req_soup(self, url):
        time_waiting = random.randint(8, 15)
        print('sleep:%is' % time_waiting)
        time.sleep(time_waiting)
        req_count = 0
        while req_count < 3:
            try:
                req_count = req_count + 1 
                headers = user_agent.get_headers()
                proxy_ip = self._proxy_pool.get()
                proxy = {'http': proxy_ip}
                resp = requests.get(url, headers=headers, timeout=self._timeout, proxies = proxy)
                break
            except Exception as ex:
                self._proxy_pool.remove(proxy_ip)
                if req_count == 3:
                    resp = requests.get(url, headers=headers, timeout=self._timeout)
                    break
            pass

        self._last_req_time = time.time()
        soup = BeautifulSoup(resp.content, 'lxml')
        return soup

    #
    def crawl_house(self, house):
        title = house.find('div', attrs={'class': 'title'}).find('a').string
        price = house.find('div', attrs={'class': 'priceInfo'}).find(
            'div', attrs={'class': 'totalPrice'}).find('span').string
        houseInfo = house.find('div', attrs={'class': 'address'}).find(
            'div', attrs={'class': 'houseInfo'})
        print('%s %s %s万' % (title, houseInfo.get_text(), price))
        self._csv_rows.append([title, houseInfo.get_text(), price])

    # 查询位置
    def scrawl_area(self, name, url):
        soup = self._req_soup(url)
        total_fl = soup.find('h2', {'class': 'total fl'}).find(
            'span').get_text()
        pages = soup.find(
            'div', attrs={'class': 'page-box house-lst-page-box'}).get('page-data')
        page_count = json.loads(pages)['totalPage']
        message = '{}共找到{}套二手房, 共{}页'.format(name, total_fl, page_count)
        print(message)
        self._csv_rows.append([message])

        idx = 1
        while True:
            houses = soup.find_all('div', attrs={'class': 'info clear'})
            for house in houses:
                self.crawl_house(house)
            if idx == page_count:
                break
            else:
                idx = idx + 1
                soup = self._req_soup(url + 'pg' + str(idx))

    # 查询区域
    def crawl_district(self, name, url):
        soup = self._req_soup(url)
        total_fl = soup.find('h2', {'class': 'total fl'}).find(
            'span').get_text()
        pages = soup.find(
            'div', attrs={'class': 'page-box house-lst-page-box'}).get('page-data')
        page_count = json.loads(pages)['totalPage']
        message = '{}共找到{}套二手房, 共{}页'.format(name, total_fl, page_count)
        print(message)
        self._csv_rows.append([message])

        areas = soup.find(
            'div', attrs={'data-role': 'ershoufang'}).find_all('div')[1].find_all('a')
        for area in areas:
            self.scrawl_area(area.string, self._url + area.get('href'))

    def crawl_ershoufang(self):
        try:
            self._csv_rows = []

            soup = self._req_soup(self._url + 'ershoufang')
            total_fl = soup.find('h2', attrs={'class': 'total fl'}).get_text()
            pages = soup.find(
                'div', attrs={'class': 'page-box house-lst-page-box'}).get('page-data')
            page_count = json.load(pages)['totalPage']
            message = '{}共找到{}套北京二手房, 共{}页'.format(total_fl, page_count)
            self._csv_rows.append([message])
            districts = soup.find(
                'div', attrs={'data-role': 'ershoufang'}).find('div').find_all('a')
            for district in districts:
                self.crawl_district(
                    district.string, self._url + district.get('href'))
        except Exception as ex:
            #print(soup.prettify())
            print('request error.')
        finally:
            self._csv_file.open('houses.csv')
            for row in self._csv_rows:
                self._csv_file.writerow(row)
            self._csv_file.close()

    def test(self):
        page = urllib.request.urlopen(self._url)
        contents = page.read()
        contents = contents.decode('utf-8', 'ignore')
        page.close()
        print(contents)


if __name__ == '__main__':
    # test
    obj = LianJia()
    obj.crawl_ershoufang()
    pass