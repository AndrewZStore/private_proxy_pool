import requests
from lxml import etree


class ProxyTest(object):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }

    def __init__(self):
        self.proxy = None

    def testWeb(self):
        url = 'https://www.zhipin.com/'
        resp = requests.get(url, proxies=self.proxy, timeout=15, headers=self.headers)
        print('status_code:', resp.status_code)
        print('text:\n', resp.text)
        print('-' * 100)

    def testHttpbinIp(self):
        url = 'http://httpbin.org/ip'
        resp = requests.get(url, proxies=self.proxy, timeout=15)
        print('status_code:', resp.status_code)
        print('text:\n', resp.text)
        print('-'*100)

    def testHttpbinHeaders(self):
        url = 'http://httpbin.org/headers'
        resp = requests.get(url, proxies=self.proxy, timeout=15)
        print('status_code:', resp.status_code)
        print('text:\n', resp.text)
        print('-' * 100)

    def testHttpbinGet(self, proxy=None):
        if proxy:
            self.proxy = proxy
            print(self.proxy)
        url = 'http://httpbin.org/get'
        try:
            resp = requests.get(url, proxies=self.proxy, timeout=15)
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

        self.proxy = {'http': 'http://' + proxy}

    def getTransparentProxy(self):
        TransparentProies = []
        url = 'https://www.kuaidaili.com/free/intr/1/'
        resp = requests.get(url, headers=self.headers, timeout=15)
        if resp.status_code != 200:
            raise Exception('fail get transparent proxy')
        html_tree = etree.HTML(resp.text)
        all_tr = html_tree.xpath('//table[@class="table table-bordered table-striped"]/tbody//tr')
        for tr in all_tr:
            try:
                ip = tr.xpath('.//td[1]/text()')[0]
                port = tr.xpath('.//td[2]/text()')[0]
                proxy = {'http': 'http://%s:%s' % (ip, port)}
                TransparentProies.append(proxy)
            except:
                pass

        return TransparentProies

proxy = '119.180.183.197:8060'
proxies = {"http": "http://" + proxy}
r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5, verify=False)
proxy_set = set()
for p in r.json()['origin'].split(','):
    proxy_set.add(p.strip())

if r.status_code == 200 and len(proxy_set) == 1 and proxy_set.pop() == proxy.split(':')[0].strip():
    print(proxy)
    print('hellow')


if __name__ == '__main__':
    # p = ProxyTest()
    # p.testHttpbinGet({"http": "http://49.51.70.42:1080"})
    # proxies = p.getTransparentProxy()
    # for proxy in proxies:
    #     p.testHttpbinGet(proxy)
    # p.getProxy('119.180.176.30:8060')
    # p.testHttpbinIp()
    # p.testHttpbinHeaders()
    # p.testWeb()
    pass

