import sys
import os

import requests
from bs4 import BeautifulSoup


class Scraper:
    url = 'https://www.nature.com'

    @staticmethod
    def error():
        print('Invalid url!')
        sys.exit()

    @staticmethod
    def set_up(url, params=None):
        input_data = requests.get(url, params=params).content if requests.get(url).status_code == 200 \
            else Scraper.error()
        input_soup = BeautifulSoup(input_data, 'html.parser')
        return input_soup

    @staticmethod
    def create_directory(page_number):
        text = f'Page_{page_number}'
        if text in os.listdir():
            Scraper.delete_directory(text)
        os.mkdir(text)

    @staticmethod
    def delete_directory(text):
        for x in os.listdir(text):
            os.remove(text + '/' + x)
        os.rmdir(text)

    @staticmethod
    def translate(title):
        translate_table = str.maketrans({' ': '_', ':': '', '?': '', ',': '', '-': ''})
        return title.translate(translate_table)

    @staticmethod
    def save_file(page_number, title, body):
        with open(f'Page_{page_number}/{title}.txt', 'wb') as f:
            f.write(body)

    def __init__(self, number_of_pages, type_of_article):
        self.number_of_pages = number_of_pages
        self.type_of_article = type_of_article
        self.page_number = 1
        self.url_dict = dict()

    def get_info(self):
        self.make_article_list()
        self.get_article_content()
        print('Save all articles.')

    def make_article_list(self):
        while self.number_of_pages >= self.page_number:
            self.url_dict[self.page_number] = []
            if self.page_number == 1:
                input_soup = Scraper.set_up(Scraper.url + '/nature/articles')
            else:
                input_soup = Scraper.set_up(Scraper.url + '/nature/articles', {'searchType': 'journalSearch', 'sort': 'PubDate', 'page': f'{self.page_number}'})
            article_link_list = [Scraper.url + x.get('href') for x in
                                 input_soup.find_all('a', class_='c-card__link u-link-inherit')]
            article_type_list = [n.text for n in input_soup.find_all('span', class_='c-meta__type')]
            counter = 0
            for x in article_type_list:
                if x == self.type_of_article:
                    self.url_dict[self.page_number].append(article_link_list[counter])
                counter += 1
            self.page_number += 1

    def get_article_content(self):
        for page_number, urls in self.url_dict.items():
            Scraper.create_directory(page_number)
            for url in urls:
                input_soup = Scraper.set_up(url)
                title_before = input_soup.find('h1').text
                title = Scraper.translate(title_before)
                search_tag = ['article__body', 'article-item__body', 'c-article-section__content']
                body = input_soup.find('div', class_=search_tag)
                if search_tag[0] == body.get('class')[0]:
                    body = ''.join([x.text for x in body.find_all(['p', 'h2'])])
                elif search_tag[1] == body.get('class')[0]:
                    body = ''.join([x.text for x in body.find_all('p')])
                else:
                    body = body.p.text
                body = body.encode('utf-8')
                Scraper.save_file(page_number, title, body)


scraper = Scraper(int(input()), input())
scraper.get_info()
