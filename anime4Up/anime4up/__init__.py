from typing import Generator
from tabulate import tabulate
from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import pandas as pd
from colorama import Style, Fore


class Anime4UP():
    ''' CLI crawler for anime4up website'''

    def __init__(self):
        self.__base_url = 'https://ww.anime4up.com/'
        self.__session = Session()
        self.__anime_status = {'مكتمل': 'Completed',
                               'يعرض الان': 'now streaming'}

    def __soup_gen(self, url: str):
        '''This Function Helps To make the code more cleaner
        '''
        req = self.__session.get(url).content
        soup = BeautifulSoup(req, features='html.parser')
        return soup

    def __page_counter(self, url: str):

        page_soup = self.__soup_gen(url)
        try:
            numbers = [num.text.strip() for num in page_soup.find_all(
                'a', class_='page-numbers')]
            nums = []
            for number in numbers:
                try:
                    i = int(number)
                    nums.append(i)
                except:
                    pass
            return sorted(nums)[-1]
        except:
            return 1

    def search(self, searchQuiery: str, save: bool = False) -> Generator:
        '''This Function Searches within the website
        if you want to save the resuts just add another argument --save
        '''
        searchq = quote_plus(searchQuiery.lower())
        url = f"{self.__base_url}?search_param=animes&s={searchq}"
        search_soup = self.__soup_gen(url)
        search_item = search_soup.find_all(
            'div', class_="col-lg-2 col-md-4 col-sm-6 col-xs-6 col-no-padding col-mobile-no-padding")
        if len(search_item) == 0:
            print(f'{Fore.RED}[*]{Style.RESET_ALL} No Results Found !')
        else:
            search_results = []
            for i, item in enumerate(search_item):
                anime_title = item.select_one(
                    'div.anime-card-details > div.anime-card-title > h3 > a').text.strip().title()
                anime_link = item.select_one(
                    'div.anime-card-details > div.anime-card-title > h3 > a').get('href')

                anime_type = item.find(
                    'div', class_='anime-card-type').find('a').text.strip().upper()

                anime_status_ar = item.find(
                    'div', class_='anime-card-status').find('a').text.strip()
                try:
                    anime_status = self.__anime_status[anime_status_ar]
                except:
                    anime_status = anime_status_ar
                search_result = {'index': i+1, 'Title': anime_title,
                                 'Type': anime_type, 'Link': anime_link, 'Status': anime_status}
                search_results.append(search_result)
                yield search_result

            if save == True:
                self.__save_results(search_results, searchQuiery)

    def __save_results(self, results: list, file_name):
        '''This is just inner function to save the results if the user added argument save
        it only saves the data into json file'''
        df = pd.DataFrame(results)
        try:
            df.to_csv(f'{file_name}.csv', index=False)
            print(
                f'{Fore.GREEN}[-]{Style.RESET_ALL} Data Saved as {file_name}.json')
            print(
                f'{Fore.GREEN}[*]{Style.RESET_ALL} A {len(results)} Record has been saved !')
            print(tabulate(results))
            return True
        except:
            return False
