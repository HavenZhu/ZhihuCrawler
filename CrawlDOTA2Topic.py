import urllib.request
from bs4 import BeautifulSoup
import ZhihuLogin
import ZHCommon


topic_number = 19638453
topic_follower_url = "https://www.zhihu.com/topic/" + str(topic_number) + "/followers"


def do_crawl():
    # 第一次请求时，使用get获取网页
    header = ZHCommon.headers
    header["Referer"] = "https://www.zhihu.com/topic/" + str(topic_number) + "/hot"
    followers = ZHCommon.session.get(topic_follower_url, headers=header)

    followers_soup = BeautifulSoup(followers.text, "html.parser")
    # 找打所有的用户信息
    users = followers_soup.find_all("div", {"class": "zm-person-item"})
    max_count = followers_soup.find("div", {"class": "zm-topic-side-followers-info"}).text[:-10].strip('\n')
    xsrf = followers_soup.find(name="input", attrs={"name": "_xsrf"}).get("value")

    mi_id = ""
    offset = 40

    for user in users:
        mi_id = user.get("id")[3:]
        print(mi_id)
        # profile_url = ZHCommon.base_url + user.find("a", {"class": "zg-link author-link"}).get("href") + "/answers"
        # user_profile = ZHCommon.session.get(profile_url, headers=ZHCommon.headers)
        # profile_soup = BeautifulSoup(user_profile.text, "html.parser")
        # user_name = profile_soup.find("span", {"class": "ProfileHeader-name"})
        # print(user_name)

    # 以后每次使用post请求来获取加载更多的数据
    do_crawl_recurse(offset=offset, start_id=mi_id, max_count=int(max_count), xsrf=xsrf)


def do_crawl_recurse(offset, start_id, max_count, xsrf):
    post_dict = {
        "offset": offset,
        "start": start_id,
        "_xsrf": xsrf
    }
    header = ZHCommon.headers
    header["Referer"] = topic_follower_url

    resp = ZHCommon.session.post(topic_follower_url, data=post_dict, headers=header)
    resp_json = resp.json()
    if resp_json["r"] == 0:
        # 获取新数据成功
        msg_count = resp_json["msg"][0]
        profiles = resp_json["msg"][1]
        followers_soup = BeautifulSoup(profiles, "html.parser")
        # 找打所有的用户信息
        users = followers_soup.find_all("div", {"class": "zm-person-item"})
        mi_id = ""
        for user in users:
            mi_id = user.get("id")[3:]
            print(mi_id)

        offset_recent = int(msg_count) + offset
        if offset_recent > 100:
            return

        if offset_recent < max_count:
            do_crawl_recurse(offset_recent, mi_id, max_count, xsrf)


if __name__ == "__main__":
    if not ZhihuLogin.is_login():
        ZhihuLogin.login("15678879734", "Zn123456")

    do_crawl()


