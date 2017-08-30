import requests


headers = {
    "Connection": "Keep-Alive",
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
}

base_url = r"https://www.zhihu.com"
login_url = r"https://www.zhihu.com/login"
session = requests.session()
