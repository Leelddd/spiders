import requests
import random
import json
import os
import codecs
import urllib
from bs4 import BeautifulSoup
from tools import proxy
from tqdm import tqdm


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

    def playlists(self, category_name: str, limit=35):
        """ get all playlist in one category """
        category = urllib.parse.quote_plus(category_name)
        url = self.url + '/discover/playlist?order=hot&cat=%s&limit=%d&offset=%d'
        try:
            url_set = set()
            html = requests.get(url % (category, 35, 0), headers=self.headers, proxies=self.get_proxy()).text
            page = int(BeautifulSoup(html, 'lxml').find_all('a', {'class': 'zpgi'})[-1].text)
            for i in range(page):
                print('getting playlist in cat %s of page %d' % (category_name, i))
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
        url = self.url + id
        playlist_map = {
            'name': lambda doc: doc.h2.text,
            'desc': lambda doc: doc.find(id='album-desc-dot').text,
            'label': lambda doc: [item.text for item in doc.find_all('a', {'class': 'u-tag'})],
            'songs': lambda doc: [li.a['href'] for li in sp.find('ul', {'class', 'f-hide'}).find_all('li')]
        }
        if field_set is None:
            field_set = set(playlist_map.keys())

        html = requests.get(url, headers=self.headers, proxies=self.get_proxy()).text
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
            # 'lyric': lambda doc, id: self.lyric(id)
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


def get_category():
    categroy_file = 'data/category.txt'
    api = NetEase([None])
    if not os.path.exists(categroy_file):
        c = api.category()
        with codecs.open(categroy_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(c))

    with codecs.open(categroy_file, 'r', encoding='utf-8') as f:
        category_list = f.readlines()
    return [item.strip() for item in category_list]


def get_playlists():
    playlist_file = 'data/playlist/'
    api = NetEase([None])
    category_list = get_category()

    for cat in category_list:
        cat_file = cat.replace('/', '')
        if os.path.exists(playlist_file + cat_file):
            continue
        lst = api.playlists(cat)
        with codecs.open(playlist_file + cat_file, 'w') as f:
            f.write('\n'.join(lst))


def get_songs(categorys):
    api = NetEase([None])

    if not os.path.exists('data/songs'):
        os.makedirs('data/songs')

    for cat in categorys:
        cat_file = 'data/songs/' + cat.replace('/', '')
        if not os.path.exists(cat_file):
            os.makedirs(cat_file)

        with codecs.open('data/playlist/' + cat.replace('/', '')) as f:
            playlists = [item.strip() for item in f.readlines()]

        for playlist in tqdm(playlists):
            # print('getting songs in playlist', playlist)
            playlist_file = cat_file + '/' + playlist.split('=')[1]
            if os.path.exists(playlist_file):
                continue
            with codecs.open(playlist_file, 'w') as f:
                f.write('\n'.join(api.playlist(playlist, ['songs'])['songs']))


def topN(n, file):
    api = NetEase([None])

    with open(file) as f:
        for i in range(n):
            id = f.readline().split('=')[-1].strip()
            print(i,api.song(id)['name'])


if __name__ == '__main__':
    """
    1. get all playlist
    2. get songs by playlist
    3. get song info
    """
    # get_playlists()
    # get_songs(['古典'])
    topN(50, 'data/songs/古典/count')
