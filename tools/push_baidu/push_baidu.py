# -*- coding: utf-8 -*-

import requests
import argparse
import xml.etree.ElementTree as ET
import os
import json
import time


ToolFolder = os.path.dirname(__file__)
ProcessFile = 'processed_dict.txt'


def LoadProcessed():
    file_name = os.path.join(ToolFolder, ProcessFile)
    processed_dict = {}
    if os.path.exists(file_name):
        with open(file_name, 'r') as input:
            processed_dict = json.load(input)

    return processed_dict


def SaveProcessed(processed_dict):
    file_name = os.path.join(ToolFolder, ProcessFile)
    with open(file_name, 'w') as output:
        json.dump(processed_dict, output)


def Run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baidu_url', type=str, default='http://data.zz.baidu.com/urls', help='baidu push url')
    parser.add_argument('--site_url', type=str, default='https://wiki.disenone.site', help='site url')
    parser.add_argument('--sitemap_url', type=str, default='https://wiki.disenone.site/sitemap.xml', help='sitemap url')
    parser.add_argument('--token', type=str, help='baidu push token')
    args = parser.parse_args()

    if not args.token:
        args.token = os.environ.get('PUSH_BAIDU_TOKEN')

    if not args.token:
        print('error: token should be pass by --token or environment variable "PUSH_BAIDU_TOKEN"')
        return parser.print_usage()

    # parse sitemap
    sitemap_ret = requests.get(args.sitemap_url, timeout=10, allow_redirects=True)
    if sitemap_ret.status_code != 200:
        raise RuntimeError('fail to visit sitemap url: %s, code: %s' % (args.sitemap_url, sitemap_ret.status_code))

    xml_root = ET.fromstring(sitemap_ret.content)

    urls = []
    for url_info in xml_root:
        for tag_info in url_info:
            if tag_info.tag.endswith('loc'):
                urls.append(tag_info.text)

    print('find url num:', len(urls))

    push_url = '%s?site=%s&token=%s' % (args.baidu_url, args.site_url, args.token)
    processed_dict = LoadProcessed()
    for url in urls:
        if url in processed_dict:
            continue
        print('pushing url:', url)
        ret = requests.post(push_url, data=url, headers={'ContentType': 'text/plain'}, timeout=10)

        print('push result:', ret.content)
        if ret.status_code != 200:
            print('push failed, status_code:', ret.status_code)
            break

        ret_info = json.loads(ret.content)
        if ret_info.get('error'):
            print('push failed')
            break

        processed_dict[url] = {'time': time.time()}

    SaveProcessed(processed_dict)


if __name__ == '__main__':
    Run()
