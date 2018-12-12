import requests as rq
import bs4

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
    "Referer": "http://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}

mozilla_header = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
}


def get_ips(num=50):
    ips = []
    url = 'http://www.xicidaili.com/nn/1'
    req = rq.get(url, headers=mozilla_header)
    soup = bs4.BeautifulSoup(req.text)
    for item in soup.find_all('tr'):
        tds = item.findAll('td')
        if len(tds) == 0:   continue
        ips.append([tds[1].contents[0], tds[2].contents[0]])
    print('get %d ips' % len(ips))
    return ips


def ip_test(ips):
    url = 'https://www.baidu.com'
    for ip in ips:
        proxy = {'proxy': 'http:\\%s:%s' % (ip[0], ip[1])}
        try:
            rq.get(url, proxies=proxy)
        except:
            print('ip:%s:%s is not available' % (ip[0], ip[1]))
            ips.remove(ip)


if __name__ == '__main__':
    ips = get_ips()
    ip_test(ips)
    print(len(ips))
    # l = list(range(10))
    # for i in l:
    #     if i % 2 == 0:
    #         l.remove(i)
    # print(l)
