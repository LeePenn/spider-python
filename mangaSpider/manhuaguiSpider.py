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

class MangaDownloadError(Exception):
    print("Manga download fail because bad internet!!!!")
    pass

# manga site domain
protocol = "https://"
domain = "www.gufengmh8.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
}
# index url
mangaIndexUrl = "www.gufengmh8.com/manhua/huayangnanziNextSeasonhuaguotianqing/"
mangaIndexUrl = quote(mangaIndexUrl)
mangaFileName = "manga_list.txt"

mangaIndexRawHtml = requests.get(protocol + mangaIndexUrl, verify=False, headers=headers, timeout=10)
if(mangaIndexRawHtml.status_code == 200):
    soup = BeautifulSoup(mangaIndexRawHtml.content, 'html.parser')
    mangaTitle = soup.find("title").get_text()

    # create manga dir
    if mangaTitle:
        # dir path
        dirPath = './' + mangaTitle + '/'
        os.makedirs(dirPath, exist_ok=True)
    # check if already download mangalist
    if os.path.isfile(dirPath + mangaFileName):
        pass
    else:
        # process html
        mangaIndexHtml = soup.find("ul", {"id": "chapter-list-1"}).find_all("li")
        mangaStr = ""
        for mangaChapter in mangaIndexHtml:
            chapterTitle = mangaChapter.find("span").get_text()
            chapterLink = protocol + domain + mangaChapter.find("a")["href"]
            mangaStr += chapterTitle + ":-:" + chapterLink + "\n"
        with open(dirPath + mangaFileName, 'w') as fh:
            fh.write(mangaStr)
            print('Success.')
else:
    print('Oops, manga index page error.')
    exit()

# download chapter
while True:
    chapterList = []
    with open(dirPath + mangaFileName, 'r') as fhC:
        for mangaChapter in fhC:
            chapterList.append(mangaChapter)

    newChapterList = chapterList

    if chapterList:
        try:
            for chapter in chapterList:
                chapterTitle = chapter.split(':-:')[0]
                # target image url
                chapterLink = chapter.split(':-:')[1].split("\n")[0]

                if (os.path.exists(dirPath + chapterTitle) == True):
                    print(dirPath + chapterTitle + ' exists')
                else:
                    os.makedirs(dirPath + chapterTitle, exist_ok=True)
                print(chapterTitle + ' start.')
                # download img
                for i in range(1,4):
                    try:
                        imageRawHtml = requests.get(chapterLink, verify=False, headers=headers, timeout=10)
                        if imageRawHtml.status_code == 200:
                            break
                    except requests.exceptions.Timeout as e:
                        print(e)
                        time.sleep(1)
                        pass
                    except requests.exceptions.ConnectionError as e:
                        print(e)
                        time.sleep(1)
                        pass
                if imageRawHtml.status_code == 200:

                    soup = BeautifulSoup(imageRawHtml.content, 'html.parser')
                    imageRawHtml = soup.find_all("script")



                    imageDomainMidPart = re.search(r'(?<=chapterPath = )\".*?\"', str(imageRawHtml[2]))
                    imageDomainMidPart = str(imageRawHtml[2])[imageDomainMidPart.span()[0]:imageDomainMidPart.span()[1]].replace("\"","")
                    imageDomainRawFirstPart = re.search(r'(?<=pageImage = )\".*?\"', str(imageRawHtml[2]))
                    imageDomainRawFirstPart = str(imageRawHtml[2])[imageDomainRawFirstPart.span()[0]:imageDomainRawFirstPart.span()[1]].replace("\"","")
                    imageDomainFirstPart = '/'.join(imageDomainRawFirstPart.split('/')[:3]) + '/'
                    imageUrl = imageDomainFirstPart + imageDomainMidPart

                    imageListStart = re.search('chapterImages = \[', str(imageRawHtml[2])).span()[1]
                    imageListEnd = re.search('\]', str(imageRawHtml[2])).span()[0]
                    imageListStr = re.sub(r"\"", "", str(imageRawHtml[2])[imageListStart:imageListEnd])
                    imageList = imageListStr.split(',')
                    pageNum = len(imageList)

                for page in range(pageNum):
                    if (os.path.isfile(dirPath + chapterTitle + '/' + str(page+1) + '.jpg')):
                        print(str(page+1) + '.jpg' + ' exists.')
                        continue
                    else:
                        for i in range(1,4):
                            try:
                                imageRawHtml = requests.get(imageUrl + imageList[page], verify=False, headers=headers, timeout=10)
                                if imageRawHtml.status_code == 200:
                                    break
                            except requests.exceptions.Timeout as e:
                                print(e)
                                time.sleep(1)
                                pass
                            except requests.exceptions.ConnectionError as e:
                                print(e)
                                time.sleep(1)
                                pass
                        if imageRawHtml.status_code == 200:
                            with open(dirPath + chapterTitle + '/' + str(page+1) + '.jpg', 'wb') as fh:
                                fh.write(imageRawHtml.content)
                                print(str(page+1) + ' success.')
                        else:
                            raise MangaDownloadError
                newChapterList = newChapterList[1:]
                newChapterStr = ""
                for newChapter in newChapterList:
                    newChapterStr += newChapter
                with open(dirPath + mangaFileName, 'w') as fh:
                    fh.write(newChapterStr)
                    print('Success.')
                break
        except MangaDownloadError:
            time.sleep(1)
            continue
    else:
        exit()





