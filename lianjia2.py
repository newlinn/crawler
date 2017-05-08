#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import json


class LianJia:
    def __init__(self):
        pass

    def get_detail(self):
        pass

    def get_house(self):
        html = self._driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        pages = soup.find(
            'div', attrs={'class': 'page-box house-lst-page-box'})
        if pages == None:
            page_count = 1
        else:
            page_data = pages.get('page-data')
            page_count = json.loads(page_data)['totalPage']

        total_fl = soup.find('h2', {'class': 'total fl'}).find(
            'span').get_text()
        message = '{}共找到{}套二手房, 共{}页'.format('name', total_fl, page_count)
        print(message)

        idx = 1
        while True:
            print(self._driver.current_url) 
            self.get_detail()
            idx = idx + 1
            if idx > page_count:
                break
            elem = self._driver.find_element_by_xpath(
                '//a[@data-page=' + str(idx) + ']')
            elem.click()
            time_waiting = random.randint(1, 5)
            print('sleepin:%i' % time_waiting)
            sleep(time_waiting) 
        pass

    def get_area(self):
        html = self._driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        areas = soup.find('div',
                          {'data-role':
                           'ershoufang'}).find_all('div')[1].find_all('a')

        total_fl = soup.find('h2', {'class': 'total fl'}).find(
            'span').get_text()
        message = '{}共找到{}套二手房, 共{}页'.format('name', total_fl, 'page_count')
        print(message)

        idx = 1
        for area in areas:
            elem = self._driver.find_element_by_xpath(
                '//div[@data-role="ershoufang"]/div[2]/a[' + str(idx) + ']')
            elem.click()
            #print(self._driver.current_url)
            self.get_house()
            idx = idx + 1
        pass

    def get_district(self):
        html = self._driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        districts = soup.find('div', {'data-role':
                                      'ershoufang'}).find('div').find_all('a')
        print('districts:%i' % len(districts))

        idx = 1
        for district in districts:
            elem = self._driver.find_element_by_xpath(
                '//div[@data-role="ershoufang"]/div[1]/a[' + str(idx) + ']')
            elem.click()
            #print(self._driver.current_url)
            self.get_area()
            idx = idx + 1
        pass

    def get_ershoufang(self):
        self._driver = webdriver.PhantomJS()
        try:
            self._driver.get('http://bj.lianjia.com/ershoufang/')
            #print(self._driver.current_url)
            self.get_district()
        except Exception as ex:
            print('Exception: %s ' % ex)
            html = self._driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            print(soup.prettify())
        self._driver.quit()
        pass


if __name__ == '__main__':
    obj = LianJia()
    obj.get_ershoufang()