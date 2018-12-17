import requests
import random
import json
from bs4 import BeautifulSoup
from tools import proxy


class NetEase:
    """
    NetEase - Basic single thread spider,
    implement get function for
        1. category;
        2. playlists in one category
        3. playlist
        4. song
        5. lyric
    """

    def __init__(self, proxies):
        self.url = 'https://music.163.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        # if proxies = [None], not use proxy
        self.proxys = [{'http': proxy} for proxy in proxies]

        if len(proxies) == 0:
            print('proxy is not enough')

    def category(self):
        """ get all categories """
        url = self.url + '/discover/playlist?order=hot'
        html = requests.get(url, headers=self.headers, proxies=self.get_proxy()).text
        return [item.text for item in BeautifulSoup(html, 'lxml').find_all('a', {'class': 's-fc1'})]

    def playlists(self, category: str, limit=35):
        """ get all playlist in one category """
        url = self.url + '/discover/playlist?order=hot&cat=%s&limit=%d&offset=%d'
        try:
            url_set = set()
            html = requests.get(url % (category, 35, 0), headers=self.headers, proxies=self.get_proxy()).text
            page = int(BeautifulSoup(html, 'lxml').find_all('a', {'class': 'zpgi'})[-1].text)
            for i in range(page):
                print('getting playlist in cat %s of page %d' % (category, i))
                html = requests.get((url % (category, limit, i * limit)), headers=self.headers,
                                    proxies=self.get_proxy()).text
                soup = BeautifulSoup(html, 'lxml')
                url_list = soup.find_all('a', {'class': 'tit'})
                for a in url_list:
                    url_set.add(a['href'])
            return list(url_set)
        except:
            return []

    def playlist(self, id: str, field_set=None):
        """ get playlist by id """
        url = self.url + '/playlist?id=%s'
        playlist_map = {
            'name': lambda doc: doc.h2.text,
            'desc': lambda doc: doc.find(id='album-desc-dot').text,
            'label': lambda doc: [item.text for item in doc.find_all('a', {'class': 'u-tag'})],
            'songs': lambda doc: [li.a['href'] for li in sp.find('ul', {'class', 'f-hide'}).find_all('li')]
        }
        field_set = set(playlist_map.keys())

        html = requests.get(url % id, headers=self.headers, proxies=self.get_proxy()).text
        sp = BeautifulSoup(html, 'lxml')
        result = {'id': id}
        for item in field_set:
            result[item] = playlist_map[item](sp)

        return result

    def song(self, id: str):
        """ get song by id """
        url = self.url + '/song?id=%s'
        song_map = {
            'name': lambda doc, id: doc.find('em', {'class': 'f-ff2'}).text,
            'players': lambda doc, id: [a['href'] for a in
                                        doc.find('p', {'class': 'des s-fc4'}).find_all('a', {'class': 's-fc7'})],
            'album': lambda doc, id: doc.find_all('p', {'class': 'des s-fc4'})[1].a.text,
            'lyric': lambda doc, id: self.lyric(id)
        }

        html = requests.get(url % id, headers=self.headers).text
        sp = BeautifulSoup(html, 'lxml')
        result = {'id': id}
        for item in list(song_map.keys()):
            result[item] = song_map[item](sp, id)
        return result

    def lyric(self, id: str):
        """ get lyric by id """
        url = self.url + '/api/song/lyric?os=pc&lv=-1&kv=-1&tv=-1&id=%s'
        return json.loads(requests.get(url % id).text)['lrc']['lyric']

    def get_proxy(self):
        """ select a random proxy in proxy list """
        return self.proxys[random.randint(0, len(self.proxys) - 1)]


def _test():
    # print(api.category())
    f = open('KTV', 'w')
    f.write(str(api.playlists('KTV')))
    f.close()
    # print(api.playlist('2467570514'))
    # print(api.song('1301256758'))


if __name__ == '__main__':
    api = NetEase([None])
    _test()
