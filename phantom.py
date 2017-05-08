#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import os
import unittest
from selenium import webdriver
from bs4 import BeautifulSoup


def test1():
    phantom_cmd = 'phantomjs phantom_req.js http://www.xdaili.cn/freeproxy.html'
    html = str(os.popen(phantom_cmd).read())
    #print('str_body:' + str_body)
    soup = BeautifulSoup(html, 'lxml')
    span = soup.find('span', {'id': 'ICP'})
    print(span.get_text())


class seleniumTest(unittest.TestCase):
    def setUp(self):
        print('setUp')
        self.driver = webdriver.PhantomJS()
        pass

    def testEle(self):
        print('testEle')
        driver = self.driver
        driver.get('http://www.douyu.com/directory/all')
        soup = BeautifulSoup(driver.page_source, 'xml')
        while True:
            titles = soup.find_all('h3', {'class': 'ellipsis'})
            nums = soup.find_all('span', {'class': 'dy-num fr'})
            for title, num in zip(titles, nums):
                print('Title:%s  NUM: %s' % (title, num))
            if driver.page_source.find('shark-pager-disable-next') != -1:
                break
            elem = driver.find_element_by_class_name('shark-pager-next')
            elem.click()
            soup = BeautifulSoup(driver.page_source, 'xml')
        pass

    def tearDown(self):
        print('tearDown')
        pass


def test_selenium():
    driver = webdriver.PhantomJS()
    try:
        driver.get('http://bj.lianjia.com/ershoufang/')
        print(driver.current_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        nav = soup.find('div', { 'data-role': 'ershoufang' })
        print(nav)
        elem = driver.find_element_by_xpath("//div[@data-role='ershoufang']/div/a[1]")
        elem.click()
        print(driver.current_url)
    except Exception as ex:
        print('Exception: %s ' % ex)    
    driver.quit()


if __name__ == '__main__':
    # unittest.main()
    # test1()
    test_selenium()
