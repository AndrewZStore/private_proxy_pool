import requests
from lxml import etree
from Manager.ProxyManager import ProxyManager
import time
from DB.DbClient import DbClient
import threading


class FreeProxyTest(object):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }

    def __init__(self):
        self.pm = ProxyManager()

    def getAll(self):
        # 获取redis数据库useful proxy
        return self.pm.getAll()

    def testWeb(self, proxy=None):
        proxies = None
        if proxy:
            proxies = {'https': 'http://' + proxy}

        url = 'https://www.zhipin.com/'
        try:
            resp = requests.get(url, proxies=proxies, timeout=10, headers=self.headers)
        except Exception as e:
            print(e)
            if proxy:
                self.pm.delete(proxy)
            return
        print('status_code:', resp.status_code)
        print('text:\n', resp.text)
        print('-' * 100)

    def testHttpbinGet(self, proxy=None):
        proxies = None
        if proxy:
            proxies = {'https': 'http://' + proxy}
        url = 'https://httpbin.org/get'
        try:
            resp = requests.get(url, proxies=proxies, timeout=10)
        except Exception as e:
            print(e)
            return
        print('status_code:', resp.status_code)
        print('text:\n', resp.text)
        print('-' * 100)

    def getProxy(self, proxy=None):
        if not proxy:
            url = 'http://127.0.0.1:5010/get/'
            resp = requests.get(url)
            if resp.status_code != 200 or resp.text == None:
                raise Exception('fail get proxy')
            proxy = resp.text
            print(proxy)

        self.proxies = {'https': 'http://' + proxy}


class PayProxyTest(object):

    def __init__(self):
        self.db = DbClient()
        self.db.changeTable('useful_proxy')

    def GetProxy(self):
        try:
            time1 = time.time()
            url = 'https://api.2808proxy.com/proxy/unify/get?token=Y3AEO9WES4U3WKQAJXZO8DYM7LAZFOQN&amount=1&proxy_type=http&format=json&splitter=rn&expire=300'
            resp = requests.get(url)
            ip = resp.json().get('data')[0].get('ip')
            http_port = resp.json().get('data')[0].get('http_port')
            proxy = '%s:%s' % (ip, http_port)
            print(proxy)
            time2 = time.time()
            print(resp.json())
            print('总耗时：', time2 - time1)
        except Exception as e:
            print(e)

    def InsertProxy(self, proxy):
        self.db.put(proxy)


if __name__ == '__main__':
    pt = FreeProxyTest()
    # proxy_list = pt.getAll()
    # for proxy in proxy_list:
    #     print(proxy)
    #     pt.testWeb(proxy)
    pt.testWeb('49.84.150.163:8883')
    pass
    # time1 = time.time()
    # p = PayProxyTest()
    # for i in range(32):
    #     p.GetProxy()
    #     time.sleep(1)
    # time2 = time.time()
    # print('总耗时：', time2 - time1)
    # p.GetProxy()

'''
status_code: 200
text:
 {
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "Ngx-Client-Ip": "118.212.200.40", 
    "User-Agent": "python-requests/2.21.0"
  }, 
  "origin": "39.134.66.13, 39.134.66.13",   39.134.66.13:8080
  "url": "https://httpbin.org/get"
}

14.115.105.236:808
status_code: 200
text:
 {
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.21.0", 
    "X-Proxy-Id": "1998266779"
  }, 
  "origin": "118.212.200.40, 14.20.235.4, 118.212.200.40", 
  "url": "https://httpbin.org/get"
}

196.13.208.23:8080
status_code: 200
text:
 {
  "args": {}, 
  "headers": {
    "Accept-Encoding": "gzip", 
    "Host": "httpbin.org", 
    "If-Modified-Since": "Thu, 28 Mar 2019 08:00:17 GMT", 
    "User-Agent": "Go-http-client/1.1"
  }, 
  "origin": "196.13.208.23, 196.13.208.23", 
  "url": "https://httpbin.org/get"
}

47.107.227.104:8888
status_code: 200
text:
 {
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Cache-Control": "max-age=259200", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.21.0"
  }, 
  "origin": "118.212.200.40, 47.107.227.104, 118.212.200.40", 
  "url": "https://httpbin.org/get"
}



status_code: 200
text:
 {
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.21.0", 
    "X-Via": "Cache-26"
  }, 
  "origin": "39.137.77.66, 39.137.77.66", 
  "url": "https://httpbin.org/get"
}

status_code: 200
text:
 {
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.21.0"
  }, 
  "origin": "61.135.180.26, 61.135.180.26", 
  "url": "https://httpbin.org/get"
}


'''
