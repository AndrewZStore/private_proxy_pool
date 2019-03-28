# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25:
-------------------------------------------------
"""
import re
import sys
import requests

try:
    from importlib import reload  # py3 实际不会实用，只是为了不显示语法错误
except:
    reload(sys)
    sys.setdefaultencoding('utf-8')

sys.path.append('..')

from Util.WebRequest import WebRequest
from Util.utilFunction import getHtmlTree
from Util.utilFunction import verifyProxyFormat

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()

"""
    data5u.com
    66ip.cn
    31f.cn
    xicidaili.com
    goubanjia.com
    kxdaili.com
    kuaidaili.com
    xsdaili.com
    zdaye.com
    ip3366.net
    iphai.com
    jiangxianli.com
    feiyiproxy.com
    qydaili.com
"""


class GetFreeProxy(object):
    """
    proxy getter
    """

    def __init__(self):
        pass

    @staticmethod
    def freeProxyFirst():
        """
        无忧代理 http://www.data5u.com/
        几乎没有能用的
        :return:
        """
        url_list = [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml'
        ]
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    yield ':'.join(ul.xpath('.//li/text()')[0:2])
                except Exception as e:
                    print(e)

    @staticmethod
    def freeProxySecond(area=34):
        """
        代理66 http://www.66ip.cn/
        :param area: 抓取代理页数，page=1北京代理页，page=2上海代理页......
        :return:
        """
        area = 34 if area > 34 else area
        for area_index in range(1, area + 1):
            url = "http://www.66ip.cn/areaindex_{}/1.html".format(str(area_index))
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath("//div[@id='footer']//table//tr[position()>1]")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0]

    @staticmethod
    def freeProxyThird():
        """
        31代理 http://31f.cn/http-proxy/
        :return:
        """
        urls = ['http://31f.cn/http-proxy/', 'http://31f.cn/https-proxy/']
        for url in urls:
            html_tree = getHtmlTree(url)
            try:
                tr_list = html_tree.xpath('//table[@class="table table-striped"]//tr[position()>1]')
                for tr in tr_list:
                    try:
                        if '天' in tr.xpath('./td[9]/text()')[0]:
                            continue
                        yield tr.xpath('./td[2]/text()')[0] + ':' + tr.xpath('./td[3]/text()')[0]
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

    @staticmethod
    def freeProxyFourth(page_count=2):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    @staticmethod
    def freeProxyFifth():
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield '{}:{}'.format(ip_addr, port)
            except Exception as e:
                pass

    @staticmethod
    def freeProxySixth():
        """
        开心代理 http://ip.kxdaili.com/dailiip.html
        :return:
        """
        urls = ['http://ip.kxdaili.com/dailiip/1/{}.html#ip'.format(str(page)) for page in range(1, 8)]
        for url in urls:
            try:
                html_tree = getHtmlTree(url)
                tr_list = html_tree.xpath('//table[@class="ui table segment"]//tbody//tr')
                for tr in tr_list:
                    try:
                        yield tr.xpath('./td[1]/text()')[0] + ':' + tr.xpath('./td[2]/text()')[0]
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

    @staticmethod
    def freeProxySeventh():
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/{page}/',
            'https://www.kuaidaili.com/free/intr/{page}/'
        ]
        for url in url_list:
            for page in range(1, 3):
                page_url = url.format(page=page)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table//tr')
                for tr in proxy_list[1:]:
                    yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxyEight():
        """
        小舒代理 http://www.xsdaili.com/
        """
        url = 'http://www.xsdaili.com/'
        html_tree = getHtmlTree(url)
        new_url = url + html_tree.xpath('//div[@class="col-md-12"]/div[1]//a[1]/@href')[0]
        new_html_tree = getHtmlTree(new_url)
        proxy_list = new_html_tree.xpath('//div[@class="cont"]/text()')
        for proxy in proxy_list:
            try:
                yield proxy.split('@')[0].strip()
            except Exception as e:
                print(e)

    @staticmethod
    def freeProxyNinth():
        """
        站大爷代理 http://ip.zdaye.com/
        :return:
        """
        url = 'http://ip.zdaye.com/'
        html_tree = getHtmlTree(url)
        item_list = html_tree.xpath('//div[@class="Loglist"]/div[2]/div[@class="panel-body"]//a/text()')
        for item in item_list:
            try:
                yield item.split('@')[0].strip()
            except Exception as e:
                print(e)

        header = {
            'Referer': 'http://ip.zdaye.com/',
        }
        new_urls = html_tree.xpath('//div[@class="Loglist"]/div[1]/div[@class="panel-body"]//a/@href')
        for new_url in new_urls:
            try:
                new_html_tree = getHtmlTree(url + new_url, header=header)
                new_item_list = new_html_tree.xpath('//div[@class="cont"]/text()')
                for new_item in new_item_list:
                    try:
                        yield new_item.split('@')[0].strip()
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

    @staticmethod
    def freeProxyTen():
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/?stype=1&page={}'.format(str(i)) for i in range(1, 4)]
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxyEleven():
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxyTwelve(page_count=8):
        """
        guobanjia http://ip.jiangxianli.com/?page=
        免费代理库
        超多量
        :return:
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0].strip() + ":" + tr.xpath("./td[3]/text()")[0].strip()

    @staticmethod
    def freeProxyThirteen():
        """
        飞蚁代理 http://www.feiyiproxy.com/?page_id=1457
        :return:
        """
        url = 'http://www.feiyiproxy.com/?page_id=1457'
        html_tree = getHtmlTree(url)
        tr_list = html_tree.xpath('//div[@class="et_pb_code et_pb_module  et_pb_code_1"]//tr[position()>1]')
        for tr in tr_list:
            yield tr.xpath('./td[1]/text()')[0].strip() + ':' + tr.xpath('./td[2]/text()')[0].strip()

    @staticmethod
    def freeProxyFourteen():
        """
        旗云代理  http://www.qydaili.com/free/?action=china&page=
        :return:
        """
        urls = ['http://www.qydaili.com/free/?action=china&page={}'.format(page) for page in range(1, 4)]
        for url in urls:
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath('//table[@class="table table-bordered table-striped"]//tbody//tr')
            for tr in tr_list:
                yield tr.xpath('./td[1]/text()')[0].strip() + ':' + tr.xpath('./td[2]/text()')[0].strip()

    @staticmethod
    def freeProxyWallFirst():
        """
        墙外网站 cn-proxy
        :return:
        """
        urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxyWallSecond():
        """
        https://proxy-list.org/english/index.php
        :return:
        """
        urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
        request = WebRequest()
        import base64
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
            for proxy in proxies:
                yield base64.b64decode(proxy).decode()

    @staticmethod
    def freeProxyWallThird():
        urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)


if __name__ == '__main__':
    from CheckProxy import CheckProxy

    CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyFourteen)
    # CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxySecond)
    #
    # CheckProxy.checkAllGetProxyFunc()

