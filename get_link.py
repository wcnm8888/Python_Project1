import requests
from lxml import etree
import os
for page in range(1, 51):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://bbs.nga.cn/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "Hm_lvt_01c4614f24e14020e036f4c3597aa059": "1744332067",
        "HMACCOUNT": "75FFC46E05300C4D",
        "ngacn0comUserInfo": "Pixel-w%09Pixel-w%0939%0939%09%0910%090%094%090%090%09",
        "ngaPassportUid": "66673785",
        "ngaPassportUrlencodedUname": "Pixel-w",
        "ngaPassportCid": "X9relbdih95e90c2paarqdf6sq9sf7c94r3plaio",
        "HM_tbj": "7gnwlr%7C16o.o0",
        "ngacn0comUserInfoCheck": "b7562b3a3394c2a9f8d9be41994351d7",
        "ngacn0comInfoCheckTime": "1744345630",
        "lastvisit": "1744346210",
        "lastpath": "/thread.php?fid=-202020",
        "bbsmisccookies": "%7B%22pv_count_for_insad%22%3A%7B0%3A-24%2C1%3A1744390812%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1744390812%7D%2C%22uisetting%22%3A%7B0%3A%22e%22%2C1%3A1744346518%7D%7D",
        "Hm_lpvt_01c4614f24e14020e036f4c3597aa059": "1744346219"
    }
    url = "https://bbs.nga.cn/thread.php"
    params = {
        "fid": "-202020",
        "page": page
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    # print(response.text)
    html = etree.HTML(response.text)
    urls = html.xpath('//a[@class="topic"]/@href')
    titles = html.xpath('//a[@class="topic"]/text()')
    print(urls)
    print(len(urls))
    if not os.path.exists('link.txt'):
        with open('link.txt', 'w', encoding='utf-8') as f:
            pass
    with open('link.txt', 'a', encoding='utf-8') as f:
        for i in range(len(urls)):
            url = 'https://bbs.nga.cn' + urls[i]
            title = titles[i]
            content = [title, url]
            f.write(str(content)+'\n')
