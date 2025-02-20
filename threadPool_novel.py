#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/7/6 14:29
import json
import requests
from concurrent.futures import ThreadPoolExecutor



def get_child_url(book_id):
    cids=[]
    url = main_url+'/getCatalog?data={"book_id":"' + book_id + '"}'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Referer': url
    }
    resp = requests.get(url, headers=header)
    result = resp.json()
    resp.close()
    data=result['data']['novel']['items']
    for item in data:
        cids.append(item['cid'])
    return cids

def download_one_page(book_id,title_id):
    data = {
        "book_id": book_id,
        "cid": f"{book_id}|{title_id}",
        "need_bookinfo": 1
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    url = main_url+'/getChapterContent?data=' + json.dumps(data)
    resp = requests.get(url, headers=header)
    result = resp.json()
    resp.close()
    title = result['data']['novel']['chapter_title']
    content = result['data']['novel']['content']
    with open(f'小说/{title}.txt', 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == '__main__':
    book_id = '4305593636'
    main_url='https://dushu.baidu.com/api/pc'
    cids=get_child_url(book_id)
    # 创建线程池
    with ThreadPoolExecutor(50) as t:
        for cid in cids:
            # 提交下载任务给线程池
            t.submit(download_one_page, book_id,cid)
    print('全部下载完毕！')