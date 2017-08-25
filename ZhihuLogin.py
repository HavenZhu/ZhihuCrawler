import requests
import urllib
import urllib.request
from bs4 import BeautifulSoup
import time
from PIL import Image
import os
import http.cookiejar as cookielib


headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
}

base_url = r"https://www.zhihu.com/"
login_url = r"https://www.zhihu.com/login/"
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_xsrf():
    try:
        html = urllib.request.urlopen(base_url).read()
        soup = BeautifulSoup(html, "html.parser")

        xsrf_input = soup.find(name="input", attrs={"name": "_xsrf"})
        xsrf = xsrf_input.get("value")
        return xsrf

    except Exception as e:
        print("can not get xsrf with error: %s" % str(e))


def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()

    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def is_login():
    profile_url = r"https://www.zhihu.com/settings/profile"
    status_code = session.get(profile_url, headers=headers).status_code
    if status_code == 200:
        return True
    else:
        return False


def login(account, password):
    xsrf = get_xsrf()
    if xsrf:
        post_dict = {
            "_xsrf": get_xsrf(),
            "password": password
        }
        if "@" in account:
            post_dict["email"] = account
            url = login_url + "email"
        else:
            post_dict["phone_num"] = account
            url = login_url + "phone_num"

        resp = session.post(url, data=post_dict, headers=headers)
        resp_json = resp.json()
        if resp_json["r"] == 1:
            # 登录失败，使用验证码登录
            captcha = get_captcha()
            post_dict["captcha"] = captcha
            resp = session.post(url, data=post_dict, headers=headers)
            resp_json = resp.json()
            print(resp_json["msg"])

        session.cookies.save()
    else:
        print("get xsrf failed")

if __name__ == "__main__":
    if not is_login():
        login("15678879734", "Zn123456")

