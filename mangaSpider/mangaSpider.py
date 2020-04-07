from bs4 import BeautifulSoup
import lxml
from urllib import request
from urllib.request import Request, urlopen
import ssl
import os
from urllib.parse import quote
import string
import re
from pprint import pprint
import json

# create dir
os.makedirs('./image/', exist_ok=True)


# ssl 表示忽略网站的不合法证书认证
ssl._create_default_https_context = ssl._create_unverified_context
# manga site domain
domain = "https://www.mh1359.com"
# index url
mangaIndexUrl = "https://www.mh1359.com/manhua/1219/"
mangaIndexUrl = quote(mangaIndexUrl, safe = string.printable)
# req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Referer': 'https://tw.manhuagui.com/comic/362/242693.html'})
request = Request(mangaIndexUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'})
mangaIndexRawHtml = urlopen(request).read().decode('utf-8')
soup = BeautifulSoup(mangaIndexRawHtml, 'html.parser')
# process html
mangaIndexHtml = soup.find("ul", {"id": "chapterList"}).find_all('a')
for chapterLink in mangaIndexHtml:
    if (os.path.exists('./image/'+chapterLink['title']) == True):
        print(chapterLink['title']+' exists')
        continue

    os.makedirs('./image/'+chapterLink['title'], exist_ok=True)
    # target chapter url
    chapterUrl = domain + chapterLink['href']
    chapterUrl = quote(chapterUrl, safe = string.printable)
    # req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Referer': 'https://tw.manhuagui.com/comic/362/242693.html'})
    request = Request(chapterUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'})
    chapterRawHtml = urlopen(request).read().decode('utf-8')
    soup = BeautifulSoup(chapterRawHtml, 'html.parser')
    # process html
    imageRawHtml = soup.find("div", {"class": "comiclist"}).find('script')
    mangaStart = re.search('chapter_list_all', imageRawHtml.contents[0]).span()[1] + 2
    mangaList = imageRawHtml.contents[0][mangaStart:].split(',')
    imageCount = 1
    # spider image loop
    for image in mangaList:
        imageStart = re.search('http', image).span()[0]
        imageEnd = re.search('middle', image).span()[1]
        imageUrl = quote(image[imageStart:imageEnd], safe = string.printable)
        # req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Referer': 'https://tw.manhuagui.com/comic/362/242693.html'})
        request = Request(imageUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        imageHtml = urlopen(request).read()
        fh = open('./image/'+str(chapterLink['title'])+'/'+str(imageCount)+'.jpg', 'wb')
        fh.write(imageHtml)
        fh.close()
        print('success')
        imageCount += 1
    print(chapterLink['title']+' ok')


exit()
