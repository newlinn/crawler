#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import random
import requests
from bs4 import BeautifulSoup
#
import user_agent


class ProxyPool:
    def __init__(self):
        self._fill()
        pass

    _timeout = 5
    _proxy_list = []

    def _fill(self):
        self._clear()
        #self._crawl_data5u() # 可用率太低
        #self._crawl_xdaili() # 需要用模拟浏览器的方式
        self._crawl_xcidaili()
        #self._crawl_kuaidaili()
        #self._crawl_haoip()#超时
        print('proxies length: %i' % len(self._proxy_list))

    def _crawl_xdaili(self):
        url = 'http://www.xdaili.cn/freeproxy.html'
        headers = user_agent.get_headers()
        resp = requests.get(url, headers=headers, timeout=self._timeout)
        print(resp)     
        if self.is_resp_valid(resp):
            soup = BeautifulSoup(resp.content, 'lxml')
            print(soup)
            trs = soup.find('tbody').find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                proxy = tds[0].string + ':' + tds[1].string
                self._insert(proxy)
        else:
            print(resp)        
                

    def _crawl_data5u(self):
        url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = user_agent.get_headers()
        resp = requests.get(url, headers=headers, timeout=self._timeout)
        if self.is_resp_valid(resp):
            soup = BeautifulSoup(resp.content, 'lxml')
            l2s = soup.find_all('ul', {'class':'l2'})
            for l2 in l2s:
                spans = l2.find_all('span')
                proxy = spans[0].find('li').string + ':' + spans[1].find('li').string
                self._insert(proxy)

    def _crawl_haoip(self):
        headers = user_agent.get_headers()
        resp = requests.get(
            'http://haoip.cc/tiqu.htm', headers=headers, timeout=self._timeout)
        soup = BeautifulSoup(resp.content, 'lxml')
        tr_list = soup.find('tbody').find_all('tr')
        for tr in tr_list:
            td_list = tr.find_all('td')
            proxy = td_list[0].string + ':' + td_list[1].string
            self._insert(proxy)

    def _crawl_kuaidaili(self):
        url = 'http://www.kuaidaili.com/free/inha/'
        print(url)
        headers = user_agent.get_headers()
        count = 0
        while (count < 5):
            count = count + 1
            resp = requests.get(
                url + str(count), headers=headers, timeout=self._timeout)
            print('url:%s' % url + str(count))
            if not self.is_resp_valid(resp):
                print('is not valid.')
                continue
            soup = BeautifulSoup(resp.content, 'lxml')
            tr_list = soup.find('tbody').find_all('tr')
            for tr in tr_list:
                td_list = tr.find_all('td')
                proxy = td_list[0].string + ':' + td_list[1].string
                self._insert(proxy)
            
    def _crawl_xcidaili(self):
        url = 'http://www.xicidaili.com/nn/'
        print(url)
        headers = user_agent.get_headers()
        count = 0
        while (count < 1):
            count = count + 1
            resp = requests.get(
                url + str(count), headers=headers, timeout=self._timeout)
            print('url:%s' % url + str(count))
            if not self.is_resp_valid(resp):
                print('is not valid.')
                continue
            soup = BeautifulSoup(resp.content, 'lxml')
            tr_list = soup.find('table').find_all('tr')
            for idx in range(1, len(tr_list)):
                td_list = tr_list[idx].find_all('td')
                proxy = td_list[1].string + ':' + td_list[2].string
                self._insert(proxy)
            
    def get(self):
        IP = random.choice(self._proxy_list)
        IP = ''.join(str(IP).strip())
        print('代理IP：%s' % IP)
        return IP

    def is_resp_valid(self, resp):
        if resp == '' or resp.status_code != 200:
            return False;
        else:
            return True        

    def _verify(self, proxy_ip):
        headers = user_agent.get_headers()
        proxies = {'http': proxy_ip}
        try:
            start_time = time.time()
            for i in range(3):
                requests.get(
                    'http://www.baidu.com',
                    headers=headers,
                    timeout=self._timeout,
                    proxies=proxies)
            time_interval = round((time.time() - start_time) / 3, 2)
            return time_interval
        except Exception as ex:
            #print(ex)
            return -1
        pass

    def _insert(self, proxy):
        time_interval = self._verify(proxy)
        if -1 < time_interval and time_interval < self._timeout:
            self._proxy_list.append(proxy)
            print('proxy: %s %ss' % (proxy, str(time_interval)))
        else:
            print('proxy: %s failed %ss' % (proxy, str(time_interval)))

    def remove(self, proxy):
        self._proxy_list.remove(proxy)
        if len(self._proxy_list) < 5:
            self._fill()

    def _clear(self):
        self._proxy_list = []


#
if __name__ == '__main__':
    start = time.strftime('%Y-%m-%d %H:%M:%S')
    print('start: %s' % start)
    proxy_pool = ProxyPool()
    end = time.strftime('%Y-%m-%d %H:%M:%S')
    print('start: %s    end: %s' % (start, end))