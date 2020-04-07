from bs4 import BeautifulSoup
import lxml
from urllib import request
from urllib.request import Request, urlopen
import ssl
import sys
from NetWork import Curl
import requests
import os
from urllib.parse import quote
import string
import re
from pprint import pprint
import json

# dir path
# dirPath = './名侦探柯南/'
# create dir
# os.makedirs(dirPath, exist_ok=True)

# ssl 表示忽略网站的不合法证书认证
ssl._create_default_https_context = ssl._create_unverified_context
# manga site domain
protocol = "https://"
domain = "www.cartoonmad.com"
# index url
mangaIndexUrl = "www.cartoonmad.com/comic/1066.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
}

mangaIndexRawHtml = Curl.curlGet(protocol + mangaIndexUrl, headers=headers, timeout=5)
if(mangaIndexRawHtml.status_code == 200):
    soup = BeautifulSoup(mangaIndexRawHtml.content, 'html.parser')
    mangaIndexHtml = soup.find("fieldset", {"id": "info"})
print(mangaIndexHtml)
exit()









# mangaIndexUrl = quote(mangaIndexUrl, safe = string.printable)


# process html

mangaIndexHtml = mangaIndexHtml[11:]
for chapterLink in mangaIndexHtml:
    pageCount = 1
    if (os.path.exists(dirPath+chapterLink.get_text()) == True):
         print(chapterLink.get_text()+' exists')
    os.makedirs(dirPath+chapterLink.get_text(), exist_ok=True)
    # target chapter url
    imageDomain = "n9.1whour.com/"
    chapterUrl = domain + chapterLink['href']

    # process html
    pageExist = 1
    while pageExist == 1:
        try:
            if (os.path.isfile(dirPath+chapterLink.get_text()+'/'+str(pageCount)+'.jpg')):
                print(str(pageCount)+'.jpg'+' exists.')
                pageCount += 1
                continue
            chapterUrlArray = chapterUrl.split('/')
            chapterUrlArray.remove(chapterUrlArray[4])
            chapterUrlArray.append(str(pageCount)+'.htm')
            chapterUrl = '/'.join(chapterUrlArray)
            # chapterUrl = quote(chapterUrl, safe = string.printable)
            chapterUrl = quote(chapterUrl)
            request = Request(protocol + chapterUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'})
            imageUrl = urlopen(request).read()

            soup = BeautifulSoup(imageUrl, 'html.parser')
            imageRawHtml = soup.find("td", {"align": "center"}).find('script')
            imageStart = re.search('\+"', imageRawHtml.contents[0]).span()[1]
            imageEnd = re.search('jpg', imageRawHtml.contents[0]).span()[1]
            imageUrl = imageDomain + imageRawHtml.contents[0][imageStart:imageEnd]
            # imageUrl = quote(imageUrl, safe = string.printable)
            imageUrl = quote(imageUrl)
            request = Request(protocol + imageUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0','Referer': 'http://comic.ikkdm.com/comiclist/369/'})
            imageUrl = urlopen(request).read()
            fh = open(dirPath+chapterLink.get_text()+'/'+str(pageCount)+'.jpg', 'wb')
            fh.write(imageUrl)
            fh.close()
            pageCount += 1
            print('success')
        except:
            print("Oops!",sys.exc_info()[0],"occured.")
            print("no that page "+chapterLink.get_text())
            pageExist = 0
    print(chapterLink.get_text()+" success")
exit()

