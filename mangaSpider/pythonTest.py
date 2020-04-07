from bs4 import BeautifulSoup
import requests
import ssl
import os
from urllib.parse import quote
import sys
import re
import time
import json
import sys

# ssl 表示忽略网站的不合法证书认证
# ssl._create_default_https_context = ssl._create_unverified_context


# manga site domain
protocol = "https://"
domain = "www.manhuagui.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
}
# index url
mangaIndexUrl = "www.2animx.com/index-look-name-%E4%B8%AD%E8%8F%AF%E5%B0%8F%E7%95%B6%E5%AE%B6-cid-14504-id-147712"
mangaIndexUrl = quote(mangaIndexUrl)
mangaFileName = "manga_list.txt"

mangaIndexRawHtml = requests.get("http://www.zerobyw4.com/plugin.php?id=jameson_manhua&a=read&zjid=68577", verify=False, headers=headers, timeout=10)

if(mangaIndexRawHtml.status_code == 200):
    with open('./test.txt', 'wb') as fh:
        fh.write(mangaIndexRawHtml.content)
        print('Success.')
        exit()
        soup = BeautifulSoup(mangaIndexRawHtml.content, 'html.parser')
        mangaTitle = soup.find("title").get_text()


