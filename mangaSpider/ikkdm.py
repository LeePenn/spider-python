from bs4 import BeautifulSoup
import lxml
from urllib import request
from urllib.request import Request, urlopen
from NetWork import Curl
import time
import requests
import ssl
import os
from urllib.parse import quote
import string
import sys
import re
from pprint import pprint
import json

# dir path
dirPath = './真相之眼/'
# create dir
os.makedirs(dirPath, exist_ok=True)

# ssl 表示忽略网站的不合法证书认证
# ssl._create_default_https_context = ssl._create_unverified_context
# manga site domain
protocol = "http://"
domain = "comic2.ikkdm.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
}
# index url
mangaIndexUrl = "comic2.ikkdm.com/comiclist/1319/index.htm"
mangaIndexUrl = quote(mangaIndexUrl)
mangaFileName = "manga_list.txt"

# check if already download mangalist
if os.path.isfile(dirPath+mangaFileName):
    pass
else:
    mangaIndexRawHtml = Curl.curlGet(protocol + mangaIndexUrl, headers=headers, timeout=5)
    if(mangaIndexRawHtml.status_code == 200):
        soup = BeautifulSoup(mangaIndexRawHtml.content, 'html.parser')
        # process html
        mangaIndexHtml = soup.find("dl", {"id": "comiclistn"}).find_all('a',attrs={"href":re.compile(r'^\/')})
    else:
        print('Oops, manga index page error.')
        exit()
    mangaStr = ""
    for mangaChapter in mangaIndexHtml:
        mangaStr += domain + mangaChapter['href'] + ":" + str(mangaChapter.get_text())+"\n"
    fh = open(dirPath+mangaFileName, 'w')
    fh.write(mangaStr)
    fh.close()
    print('Success.')

fhC = open(dirPath+mangaFileName, 'r')
mangaList = []
for mangaChapter in fhC:
    mangaList.append(mangaChapter)
fhC.close()
# mangaIndexUrl = quote(mangaIndexUrl, safe = string.printable)

# mangaList = mangaList[19:]
# download chapter
if mangaList:
    for chapterLink in mangaList:
        chapterLink = chapterLink.split(':')
        name = chapterLink[1].split("\n")
        name = name[0]
        pageCount = 1
        if (os.path.exists(dirPath+name) == True):
            print(dirPath+name+' exists')
        os.makedirs(dirPath+name, exist_ok=True)
        # target chapter url
        imageDomain = "n2.1whour.com/"

        # process html
        pageExist = 1
        while pageExist == 1:
            if (os.path.isfile(dirPath+name+'/'+str(pageCount)+'.jpg')):
                print(str(pageCount)+'.jpg'+' exists.')
                pageCount += 1
                continue
            chapterUrlArray = chapterLink[0].split('/')
            chapterUrlArray.remove(chapterUrlArray[4])
            chapterUrlArray.append(str(pageCount)+'.htm')
            chapterUrl = '/'.join(chapterUrlArray)
            # chapterUrl = quote(chapterUrl, safe = string.printable)
            chapterUrl = quote(chapterUrl)

            # print(chapterUrl)
            # exit()
            for i in range(1,4):
                try:
                    imageUrl = requests.get(protocol + chapterUrl, headers=headers, timeout=5)
                    # imageUrl = requests.get("http://comic2.ikkdm.com/comiclist/2197/52952/3.htm", headers=headers, timeout=5)
                    if imageUrl.status_code == 200 or 404:
                        break
                except requests.exceptions.Timeout:
                    time.sleep(3)
                    pass
                except requests.exceptions.ConnectionError:
                    time.sleep(3)
                    pass
            if imageUrl.status_code == 404:
                break
            if imageUrl.status_code == 200:
                soup = BeautifulSoup(imageUrl.content, 'html.parser')
                # process html
                imageRawHtml = soup.find("td", {"align": "center"}).find('script')

                imageStart = re.search('\+"', imageRawHtml.contents[0]).span()[1]
                imageEnd = re.search(r'(jpg)|(png)|(gif)', imageRawHtml.contents[0], re.IGNORECASE).span()[1]

                imageUrl = imageDomain + imageRawHtml.contents[0][imageStart:imageEnd]

                # print(imageUrl)
                # exit()
                # imageUrl = quote(imageUrl, safe = string.printable)
                imageUrl = quote(imageUrl)

                for i in range(1,4):
                    try:
                        # print(imageUrl)
                        # exit()
                        imageUrl = requests.get(protocol + imageUrl, headers=headers, timeout=5)
                        # imageUrl = requests.get("http://n9.1whour.com/comic/kuku2comic/wqwz/Vol_05/ThePrinceofTennis_05_148.jpg", headers=headers, timeout=5)
                        if imageUrl.status_code == 200:
                            break
                    except requests.exceptions.Timeout:
                        time.sleep(3)
                        pass
                    except requests.exceptions.ConnectionError:
                        time.sleep(3)
                        pass
                if imageUrl.status_code != 200:
                    print(str(pageCount)+" fail.")
                    exit()
                else:
                    fh = open(dirPath+name+'/'+str(pageCount)+'.jpg', 'wb')
                    fh.write(imageUrl.content)
                    fh.close()
                    pageCount += 1
                    print(str(pageCount) + ' success.')
                # print("Oops!",sys.exc_info()[0],"occured.")
                # print("no that page "+chapterLink.get_text())
                # pageExist = 0
        print(name+" success")
exit()

