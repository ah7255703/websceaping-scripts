'''This is akwam module to scrape from akwam.com'''

__author__ = 'Ahmed Hassan'
__version__ = '0.1'

from bs4 import BeautifulSoup
import requests
import re

from urllib.parse import quote_plus
from colorama import Fore, Style


class Akwam():
    '''This is the Base Class for Our Module\n
    This Class Will help You to easily generate Download 
    links for akwam media without ads
    '''
    __base_url: str
    __categories: list

    def __init__(self):
        self.__base_url = "https://akwam.cx/"
        self.__categories = ['movies', 'series', 'games']

    def __soup_gen(self, url):
        'This Function Will return the soup object'
        request = requests.get(url).content
        return BeautifulSoup(request, features='html.parser')

    def __pages_count(self, url):
        soup_page = self.__soup_gen(url)
        ss = soup_page.find_all('a', class_='page-link')
        l = []
        for i in ss:
            try:
                n = int(i.text)
                l.append(n)
            except:
                pass
        l.sort()
        try:
            return l[-1]
        except:
            return 1

    def grapper(self, cat: str):
        '''This Function Will get every item in the category
        [movies,games,series,programs,mix]
        Usage grapper 'category_name'
        '''
        pages_count_all = self.__pages_count(self.__base_url + cat)
        while True:
            pages_count = int(input(
                f'{Fore.GREEN}[?]{Style.RESET_ALL} How Many Pages Do You Want To show ? |There are [{pages_count_all}] pages| ').strip())
            if pages_count > pages_count_all:
                print(
                    f'{Fore.RED}[!] {Style.RESET_ALL}The requested page doesnt Exist \n')
                continue
            else:
                break

        for i in range(1, pages_count + 1):
            print(
                f'{Fore.GREEN}[-] {Style.BRIGHT}Page {i} Of {pages_count}{Style.RESET_ALL}')
            soup = self.__soup_gen(
                self.__base_url + cat + '?page={}'.format(i))
            items = soup.select(
                'body > div.site-container > div.page.page-archive > div.container > div.widget > div > div > div > div.entry-body.px-3.pb-3.text-center > h3 > a')

            for index, item in enumerate(items):
                yield {'index': index, 'Title': item.text, 'Link': item.get('href'), 'Category': cat}

    def searcher(self, search_Quiery: str):
        '''This Function Will apply Search quiery and get 
        the links and title of akwam media'''
        string = quote_plus(search_Quiery.lower())
        url = self.__base_url + 'search?q={}'.format(string)
        pages_num = self.__pages_count(url)
        for i in range(1, pages_num+1):
            soup = self.__soup_gen(url + '&page={}'.format(i))
            search_items = soup.select(
                'body > div.site-container > div.page.page-search > div.container > div.widget > div > div > div')
            if len(search_items) == 0:
                print(f'{Fore.RED}[*]{Style.RESET_ALL} No Results Found !')
            else:
                print(
                    f'{Fore.GREEN}[*] Page {i}{Style.RESET_ALL} Of {Fore.CYAN}{pages_num}{Style.RESET_ALL}')

                for n, i in enumerate(search_items):
                    Title = i.select_one(
                        'div.entry-body.px-3.pb-3.text-center > h3 > a').text.strip()
                    Link = i.select_one(
                        'div.entry-body.px-3.pb-3.text-center > h3 > a').get('href')
                    cat = Link.split('/')[3]
                    if cat == 'movie':
                        quality = i.find(
                            'span', class_='label quality').text.strip()
                        yield {'index': n, 'Title': Title, 'Link': Link, 'category': cat, 'Movie Quality': quality}
                    else:
                        yield {'index': n, 'Title': Title, 'Link': Link, 'category': cat}

    def __ads_bybasser(self, url):
        soup = self.__soup_gen(url)
        i = soup.select_one(
            'body > div.site-container > div > div.content > a').get('href')
        soup_i = self.__soup_gen(i)
        return soup_i.select_one('body > div.site-container > div.page-redirect > div > div > div > p > a').get('href')

    def fetcher(self, url):
        'This Function Will return{thumbnail , title , etc..} and direct Download links for this media'
        category = url.split('/')[3]
        if category == 'games':
            print(
                f'{Fore.RED}[-]{Style.RESET_ALL} game is not supported within this function Try game_fetcher Function')
        else:
            item_soup = self.__soup_gen(url)

            Title = item_soup.select_one(
                'body > div.site-container > div.page.page-movie.page-film > div.movie-cover.mb-4.without-cover > div > div > div.col-lg-7.pr-lg-4.col-md-5.col-sm-8.mb-4.mb-sm-0.px-4.px-sm-0 > h1').text.strip().title()
            idmb_rate = item_soup.select_one(
                'body > div.site-container > div.page.page-movie.page-film > div.movie-cover.mb-4.without-cover > div > div > div.col-lg-7.pr-lg-4.col-md-5.col-sm-8.mb-4.mb-sm-0.px-4.px-sm-0 > div.font-size-16.text-white.mt-2.d-flex.align-items-center > span.mx-2').text.strip()
            try:
                year_production = item_soup.select_one(
                    'body > div.site-container > div.page.page-movie.page-film > div.movie-cover.mb-4.without-cover > div > div > div.col-lg-7.pr-lg-4.col-md-5.col-sm-8.mb-4.mb-sm-0.px-4.px-sm-0 > div:nth-child(7) > span').text.strip().split(':')[1]
            except:
                year_production = None
            # the staff
            staff_tags = item_soup.select(
                'body > div.site-container > div.page.page-movie.page-film > div.container > div > div > div > div > a > div.col > div')
            staff_names = [i.text.strip() for i in staff_tags]
            if category == 'movie':

                download_links = self.ID_links_gen(url)
                return {'Title': Title, 'IDMB': idmb_rate, 'Year': year_production, 'Staff': staff_names, 'Download': download_links}
            if category not in self.__categories:

                print(f'{Fore.RED}[*] {Fore.GREEN}Not Supported Yet !')

            # Series
            if category == 'series':

                episodes_urls = [i.get('href') for i in item_soup.select(
                    '#series-episodes > div > div > div > h2 > a')]
                print(
                    f'{Fore.GREEN}[*]{Style.RESET_ALL}The Requested Series Title is : {Title} ,The Idmb rate is {idmb_rate} \n episodes Count {len(episodes_urls)} \n Do You Want To Fetch all Episodes (Enter For Yes) or enter specefic number|')

                while True:
                    count = input(
                        f'{Fore.GREEN}[*] {Style.RESET_ALL}Choose from {len(episodes_urls)} :')
                    try:
                        if int(count) > len(episodes_urls) and count != "":
                            continue
                    except:
                        pass
                    if count == "":
                        count = len(episodes_urls)
                        break

                episode_D_links = []
                for i, item in enumerate(episodes_urls[0:int(count)]):
                    D_links = self.ID_links_gen(item)
                    episode_D_links.append({i+1: D_links})
                return {'Title': Title, 'IDMB Rate': idmb_rate, 'Year Of Production': year_production, f'{Fore.GREEN}[*]{Style.RESET_ALL} Download Links': episode_D_links}

    def ID_links_gen(self, url):
        '''this function as well as ads bybasser will get the download links for the media
        If You Already Have The url For The movie or episode of the series this function will 
        return back the direct download links
        '''
        ID_soup = self.__soup_gen(url)
        links_tags = ID_soup.find_all('a', class_=re.compile('download'))
        D_links = []
        for i in links_tags:
            size = i.text.strip().replace('تحميل', '')
            indirect_link = i.get('href')
            D_links.append({size: self.__ads_bybasser(indirect_link)})
        return D_links

    def game_fetcher(self, url: str):
        'This Function Deals With Games in the website it can Fetch the direct Download Link within the website'
        category = url.split('/')[3]
        if category != 'games':
            print('Not Supported,Try To use Fetcher Function')
        else:
            game_soup = self.__soup_gen(url)
