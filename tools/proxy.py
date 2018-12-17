import requests as rq
import bs4
import os
from concurrent.futures import ThreadPoolExecutor
import timeit


class Proxy:

    def __init__(self):
        self.proxy_hosts = [self.xicidaili]
        self.file = 'proxy.txt'
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
        }

    def get_proxy(self, num=50):
        """ get proxies by some proxy hosts """
        proxy_file = 'proxy.txt'
        if os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                proxies = self.valid_filter(f.readlines())
        else:
            proxies = []

        print("proxy not enough, start get...")
        if len(proxies) < num:
            for host in self.proxy_hosts:
                ps = host()
                t1 = timeit.default_timer()
                proxies.extend(self.valid_filter(ps))
                t2 = timeit.default_timer()
                print(t2 - t1)
                if len(proxies) >= num:
                    self.save(proxies)
                    break

        if len(proxies) < num:
            print("Can not get enough proxies currently, need %d, get %d, please try again later..." % (
                num, len(proxies)))
            raise Exception()

        return proxies

    def valid_filter(self, proxies):
        """ select valid proxy in proxy list """
        with ThreadPoolExecutor(len(proxies)) as exector:
            valids = exector.map(self.test, proxies)
            return [proxies[i] for i, valid in enumerate(valids) if valid]

    def test(self, proxy: str):
        """ check if a proxy is valid """
        print('check proxy:', proxy)
        url = 'http://www.baidu.com'
        try:
            rq.get(url, proxies={'http': proxy}, timeout=5)
        except:
            print('proxy: %s is not valid' % proxy)
            return False
        print('proxy: %s is valid' % proxy)
        return True

    def save(self, proxies):
        with open(self.file, 'w') as f:
            f.write('\n'.join(proxies))

    # ======================================================================================================================
    # some proxy spiders

    def xicidaili(self):
        """ spider for xicidaili.com """
        ips = []
        for i in range(3):
            url = 'http://www.xicidaili.com/nn/%d' % i
            req = rq.get(url, headers=self.headers, timeout=5)
            soup = bs4.BeautifulSoup(req.text)
            for item in soup.find_all('tr'):
                tds = item.findAll('td')
                if len(tds) == 0:   continue
                ips.append("%s://%s:%s" % (tds[5].contents[0].lower(), tds[1].contents[0], tds[2].contents[0]))
        print('get %d ips' % len(ips))
        return ips

    # def kuaidaili(self):
    #     """ spider for kuaidaili.com """
    #     ips = []



if __name__ == '__main__':
    p = Proxy()
    p.get_proxy()
