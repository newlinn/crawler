#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import user_agent

def test1():  
    url = 'https://bj.lianjia.com/ershoufang/shunyi/'
    headers = user_agent.get_headers()
    resp = requests.get(url, headers=headers, timeout=5)
    soup = BeautifulSoup(resp.content, 'lxml')
    #print(soup.prettify())
    houses = soup.find_all('div', attrs={'class': 'info clear'})
    houseInfo = houses[0].find('div', attrs={'class': 'address'}).find('div', attrs={'class': 'houseInfo'})
    print(houseInfo)
    print(houseInfo.get_text()) 

def doCallback(txt):
    print('doCallback:' + txt)

def test2(callback):
    callback('text2')

test2(doCallback)