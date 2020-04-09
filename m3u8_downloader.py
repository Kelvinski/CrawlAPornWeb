# coding=utf-8

"""
这里根据列表，请求到 m3u8文件
有的文件需要二次请求
因此获取真实 m3u8文件

"""

import os
import re
import time
import requests
from config import HEADERS_LIST, PROXY_PRO

FILE_LIST = [i for i in os.listdir('./list')]


def view_all_list():
    for path in FILE_LIST:
        for i in open(''.join(['./list/', path]), 'r', encoding='utf-8'):
            info = i.strip().split('\u0001')
            info[-1] = path.split('_')[0]
            lets_get_m3u8_file(info)
            

def lets_get_m3u8_file(info):
    title, url, cate = info
    print('当前是:\t', cate, title, url)
    if not os.path.exists('./m3u8/{0}/{1}/'.format(cate, title)):
        print('目录不存在，创建目录:', './{0}/{1}/'.format(cate, title))
        os.makedirs('./m3u8/{0}/{1}/'.format(cate, title))
    print('下载详情页面，搜索 m3u8 地址..')
    html = download_m3u8_url(url)
    m3u8_link = parse_m3u8(html)
    print('当前 m3u8地址为:\t{0}\t开始处理'.format(m3u8_link))
    deal_m3u8(m3u8_link, './m3u8/{0}/{1}/'.format(cate, title))


def deal_m3u8(url, file_path):
    # 这里需要看第一次下载的m3u8是否可用,是否需要新的跳转
    print('开始下载文件')
    m3u8 = download_m3u8_file(url)
    if 'index.m3u8' in m3u8:
        # 说明要重新下载新的
        print('进对比,需要二次下载')
        path = re.findall('(\d.*/index.m3u8)', m3u8)[0]
        print('解析出的新地址:\t{0}'.format(path))
        new_url = url.split('index')[0] + path
        print('新的m3u8地址{0}\t开始下载'.format(new_url))
        m3u8 = download_m3u8_file(new_url)
    save_path = ''.join([file_path, 'index.m3u8'])
    print('保存目录:\t{0}'.format(save_path))
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(m3u8)


def download_m3u8_file(url):
    html = None
    retry = 5
    while retry > 0:
        try:
            if PROXY_PRO:
                resp = requests.get(url, proxies=PROXY_PRO)
            else:
                resp = requests.get(url)
            if resp.status_code < 300:
                html = resp.content.decode('utf-8')
                break
        except Exception as e:
            print('请求出错,', e)
            time.sleep(5)
        retry -= 1
    return html


def download_m3u8_url(url):
    html = None
    retry = 5
    while retry > 0:
        try:
            if PROXY_PRO:
                resp = requests.get(url, headers=HEADERS_LIST, proxies=PROXY_PRO)
            else:
                resp = requests.get(url, headers=HEADERS_LIST)
            if resp.status_code < 300:
                html = resp.content.decode('utf-8')
                break
        except Exception as e:
            print('请求出错,', e)
            time.sleep(5)
        retry -= 1
    return html


def parse_m3u8(html):
    m3u8 = re.findall('Play=(http.*?m3u8)', html, re.S)[0]
    return m3u8


if __name__ == '__main__':
    view_all_list()