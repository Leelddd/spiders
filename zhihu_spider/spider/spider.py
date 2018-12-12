import json
import requests as rq
from bs4 import BeautifulSoup, SoupStrainer
from zhihu_spider.spider.proxy import get_ips, headers

user_queue = []


def basic_info(token: str):
    """
    get followers, followees, answer, questions, articles, columns, think, get_like, public_edit ,collected_answer,
    :param token:
    :return:
    """
    info = {}
    url = 'https://www.zhihu.com/people/%s/activities' % token
    r = rq.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    # follow board
    follow = soup.find_all('strong', {'class': 'NumberBoard-itemValue'})
    info['followee'] = follow[0].text
    info['follower'] = follow[1].text

    # number tab
    tabs = soup.find_all('li', {'class': 'Tabs-item'})
    # answer
    info['answer'] = tabs[1].find('span', {'class': 'Tabs-meta'}).text
    # question
    info['question'] = tabs[2].find('span', {'class': 'Tabs-meta'}).text
    # article
    info['article'] = tabs[3].find('span', {'class': 'Tabs-meta'}).text
    # column
    info['column'] = tabs[4].find('span', {'class': 'Tabs-meta'}).text
    # think
    info['question'] = tabs[4].find('span', {'class': 'Tabs-meta'}).text


def get_followees_by_token(token):
    url = "https://www.zhihu.com/api/v4/members/%s/followees?limit=20&offset=0" % token
    r = rq.get(url, headers=headers)
    json.loads(r.text)


def get_followees(token: str, offset: int, limit: int):
    url = "https://www.zhihu.com/api/v4/members/%s/followees?limit=%d&offset=%d" % (token, limit, offset)
    r = rq.get(url, headers=headers)
    json.loads()


# ==========================================================================================================
# tools


# r = rq.get('https://www.zhihu.com/people/Ashes-of-Time/followers', headers=headers)
# print(r.text)

# r = rq.get('http://api.xicidaili.com/free2016.txt')
# print(r.text)

if __name__ == '__main__':
    basic_info('columbia')
    # ips = get_ips()
    # ip_test(ips)
    # print(len(ips))
    # l = list(range(10))
    # for i in l:
    #     if i % 2 == 0:
    #         l.remove(i)
    # print(l)
