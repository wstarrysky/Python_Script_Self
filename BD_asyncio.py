"""
可以实现一页一页的异步爬取图片，且效果比较稳定
"""

import asyncio
import re
import time
import aiohttp
import requests
import argparse
from urllib.parse import urlencode
from fake_useragent import UserAgent


ua = UserAgent()

headers = {
    'Connection': 'close',
    'User-Agent': str(ua.random),
    'Cookie': "BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm"
}


async def downloader(name, img):
    file_name = 'images_src/' + f"{name}.jpg"
    async with aiohttp.ClientSession() as session:
            resp = await session.get(img)
            # response.raise_for_status()
            with open(file_name, 'wb') as f:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    f.flush()
    print('下载成功!' + file_name)



def get_base_url(keyword, i):
    params = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'ct': '201326592',
        'is': '',
        'fp': 'result',
        'queryWord': f'{keyword}',
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '-1',
        'z': '',
        'ic': '0',
        'hd': '',
        'latest': '',
        "copyright": '',
        'word': f'{keyword}',
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': '0',
        'istype': '2',
        'qc': '',
        'nc': '1',
        'fr': '',
        'expermode': '',
        'cg': 'girl',
        'nojc': '',
        'pn': i*30,
        'rn': '30',
        'gsm': '5a',
        '1627704634095': '',
    }
    # https://image.baidu.com/search/acjson?tn=resultjson_com
    # &logid=11488366300915428523
    url = 'https://image.baidu.com/search/acjson?' + urlencode(params)
    return url


def baidtu_uncomplie(url):
    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d = {'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e', 'u': 'f', '2': 'g', 'i': 'h', 't': 'i', '3': 'j', 'h': 'k',
         's': 'l', '4': 'm', 'g': 'n', '5': 'o', 'r': 'p', 'q': 'q', '6': 'r', 'f': 's', 'p': 't', '7': 'u', 'e': 'v',
         'o': 'w', '8': '1', 'd': '2', 'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7', 'b': '8', 'l': '9', 'a': '0',
         '_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
    if (url == None or 'http' in url):
        return url
    else:
        j = url
        for m in c:
            j = j.replace(m, d[m])
        for char in j:
            if re.match('^[a-w\d]+$', char):
                char = d[char]
            res = res + char
        return res


def run(number, keyword):
    count = 0
    for i in range(1, number + 1):
        print(f'********************************第{i}页*****************************************************\n')
        start = time.time()  # 记录起始时间戳
        base_url = get_base_url(keyword, i)
        image_json = requests.get(base_url, headers=headers).json()
        image_list = []
        for img in image_json['data']:
            try:
                img_url = baidtu_uncomplie(img['objURL'])
                image_list.append(img_url)
            except:
                continue
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(downloader(f"{keyword}_{i}_{k+1}", image)) for k, image in
                 enumerate(image_list)]
        loop.run_until_complete(asyncio.wait(tasks))
        end = time.time()  # 获取结束时间戳
        print(f'下载第{i}页共用了{end - start}秒\n')  # 程序耗时


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="偷图懒人脚本")
    parser.add_argument('-n', '--number', type=int, default=4, help="预期下载的页数(一页30张)")
    args = parser.parse_args()

    keyword = input("输入关键词")

    run(args.number, keyword)
