import base64
import json
import re
import sys

import requests

client = requests.Session()


import re
import requests

import urllib.parse



# search_url = f"https://xxx.com/search_lyrics?title={trackTitle}&artist={artist}&album={album}"
search_url = f"https://mora.jp/getLyrics?_=1684138707614&materialNo=22563653"


client.headers.clear()
client.headers['Accept'] = '*/*'
client.headers['Accept-Language'] = 'ja'
client.headers['Referer'] = "https://mora.jp/package/43000011/4580789508790_HD/"
client.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko'
client.headers['Pragma'] = 'no-cache'
client.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
client.headers['X-Requested-With'] = 'XMLHttpRequest'

response = client.post(search_url)
print(response.text)