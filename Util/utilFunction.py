# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     utilFunction.py
   Description :  tool function
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 添加robustCrawl、verifyProxy、getHtmlTree
-------------------------------------------------
"""
import requests
import time
from lxml import etree

from Util.LogHandler import LogHandler
from Util.WebRequest import WebRequest

logger = LogHandler(__name__, file=False)


# noinspection PyPep8Naming
def robustCrawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass
            # logger.info(u"sorry, 抓取出错。错误原因:")
            # logger.info(e)

    return decorate


# noinspection PyPep8Naming
def verifyProxyFormat(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


# noinspection PyPep8Naming
def getHtmlTree(url, header=None, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """

    headers = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    if header and isinstance(header, dict):
        headers.update(header)
    # TODO 取代理服务器用代理服务器访问
    wr = WebRequest()

    # delay 2s for per request
    time.sleep(2)

    html = wr.get(url=url, header=headers).content
    return etree.HTML(html)


def tcpConnect(proxy):
    """
    TCP 三次握手
    :param proxy:
    :return:
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False


# noinspection PyPep8Naming
def validUsefulProxy(proxy):
    """
    检验代理是否可用,以及是否为高匿
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    # TODO 编写设置，测试http代理还是测试https代理
    # TODO 测试代理，以自定义的url进行测试
    proxies = {"https": "http://{proxy}".format(proxy=proxy)}
    try:
        # 超过5秒的代理就不要了，不是高匿的代理也不要
        r = requests.get('https://httpbin.org/get', proxies=proxies, timeout=5, verify=False)
        headers = r.json().get('headers')
        if not headers:
            raise Exception('fail get headers:', proxy)
        if headers.get('Ngx-Client-Ip', None):
            raise Exception('Transparent proxy:', proxy)
        if headers.get('Cdn-Src-Ip', None):
            raise Exception('Transparent proxy')
        if headers.get('X-Via', None):
            raise Exception('Ordinary anonymity proxy', proxy)
        if headers.get('X-Proxy-Id', None):
            raise Exception('Ordinary anonymity proxy', proxy)

        proxy_set = set()
        for p in r.json().get('origin').split(','):
            proxy_set.add(p.strip())

        if len(proxy_set) != 1:
            raise Exception('Not hign anonymity proxy:', proxy)

        return True
    except Exception as e:
        logger.info(str(e))
        return False
