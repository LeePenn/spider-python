import requests

def curlGet(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',}, timeout = 5):
    return requests.get(url, headers=headers, timeout=timeout)