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
domain = "manhua.fzdm.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
}
# index url
mangaIndexUrl = "manhua.fzdm.com/89/"
mangaIndexUrl = quote(mangaIndexUrl)
mangaFileName = "manga_list.txt"

mangaIndexRawHtml = requests.get(protocol + mangaIndexUrl, verify=False, headers=headers, timeout=10)
if(mangaIndexRawHtml.status_code == 200):
    soup = BeautifulSoup(mangaIndexRawHtml.content, 'html.parser')
    mangaTitle = soup.find("meta", {"property": "og:novel:book_name"})
    # create manga dir
    if mangaTitle['content']:
        # dir path
        dirPath = './' + mangaTitle['content'] + '/'
        os.makedirs(dirPath, exist_ok=True)
    # check if already download mangalist
    if os.path.isfile(dirPath + mangaFileName):
        pass
    else:
        # process html
        mangaIndexHtml = soup.find_all("li", {"class": "pure-u-1-2 pure-u-lg-1-4"})
        mangaStr = ""
        for mangaChapter in mangaIndexHtml:
            chapterTitle = mangaChapter.find("a")['title']
            chapterLink = protocol + mangaIndexUrl + mangaChapter.find("a")['href']
            mangaStr += mangaChapter.find("a")['title'] + ":-:" + protocol + mangaIndexUrl + mangaChapter.find("a")['href'] + "\n"
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

    # splitChapter = sys.argv[1]
    # chapterList = chapterList[int(splitChapter):]
    newChapterList = chapterList

    if chapterList:
        try:
            imageDomain = "http://p1.manhuapan.com/"
            for chapter in chapterList:
                chapterName = chapter.split(':-:')[0]
                # target image url
                chapterLink = chapter.split(':-:')[1].split("\n")[0]
                if (os.path.exists(dirPath + chapterName) == True):
                    print(dirPath + chapterName + ' exists')
                else:
                    os.makedirs(dirPath + chapterName, exist_ok=True)
                page = 1
                pageExist = True
                while pageExist:
                    if (os.path.isfile(dirPath + chapterName + '/' + str(page)+'.jpg')):
                        print(str(page) + '.jpg' + ' exists.')
                        page += 1
                        continue
                    # elif page==144 or page==145:
                    #     print(str(page) + 'pass')
                    #     page += 1
                    #     continue
                    else:
                        if page == 1:
                            # download img
                            for i in range(1,4):
                                try:
                                    imageRawHtml = requests.get(chapterLink, verify=False, headers=headers, timeout=10)
                                    if imageRawHtml.status_code == 200 or 500:
                                        break
                                except requests.exceptions.Timeout as e:
                                    print(e)
                                    time.sleep(1)
                                    pass
                                except requests.exceptions.ConnectionError as e:
                                    print(e)
                                    time.sleep(1)
                                    pass
                        else:
                            # download img
                            for i in range(1,4):
                                try:
                                    imageRawHtml = requests.get(chapterLink + 'index_' + str(page - 1) + '.html', verify=False, headers=headers, timeout=10)
                                    if imageRawHtml.status_code == 200 or 500:
                                        break
                                except requests.exceptions.Timeout as e:
                                    print(e)
                                    time.sleep(1)
                                    pass
                                except requests.exceptions.ConnectionError as e:
                                    print(e)
                                    time.sleep(1)
                                    pass
                        try:
                            if imageRawHtml.status_code == 200:
                                soup = BeautifulSoup(imageRawHtml.content, 'html.parser')
                                imageRawHtml = soup.find_all("script")

                                imageStart = re.search('mhurl="', str(imageRawHtml[11])).span()[1]
                                imageEnd = re.search('jpg', str(imageRawHtml[11]))
                                if imageEnd == None:
                                    print(chapterName + ' finish.')
                                    break
                                else:
                                    imageLink = imageDomain + str(imageRawHtml[11])[imageStart:imageEnd.span()[1]]
                                # download image
                                for i in range(1,4):
                                    try:
                                        imageUrl = requests.get(imageLink, headers=headers, timeout=10)
                                        if imageUrl.status_code == 200 or 500:
                                            break
                                    except requests.exceptions.Timeout as e:
                                        print(e)
                                        time.sleep(1)
                                        pass
                                    except requests.exceptions.ConnectionError as e:
                                        print(e)
                                        time.sleep(1)
                                        pass
                                if imageUrl.status_code == 200:
                                    with open(dirPath + chapterName + '/' + str(page) + '.jpg', 'wb') as fh:
                                        fh.write(imageUrl.content)
                                        print(str(page) + ' success.')
                                        page += 1
                                        time.sleep(1)
                                else:
                                    print(chapterName + ' finish.')
                                    break
                            elif imageRawHtml.status_code == 500:
                                print(chapterName + ' finish.')
                                newChapterList = newChapterList[1:]
                                newChapterStr = ""
                                for newChapter in newChapterList:
                                    newChapterStr += newChapter
                                with open(dirPath + mangaFileName, 'w') as fh:
                                    fh.write(newChapterStr)
                                    print('Success.')
                                break
                            else:
                                raise MangaDownloadError
                        except AttributeError:
                            raise MangaDownloadError

        except MangaDownloadError:
            time.sleep(1)
            continue
    else:
        exit()





