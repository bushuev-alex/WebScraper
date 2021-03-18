import requests

from bs4 import BeautifulSoup

page_number = int(input())
url_link = input()

# page_number = 3
# url_link = 'http://www.gutenberg.org/files/3825/3825-h/3825-h.htm'

r = requests.get(url_link, headers={'Accept-Language': 'en-US,en;q=0.5'})
soup = BeautifulSoup(r.content, 'html.parser')
all_hrefs_list = soup.find_all('a')

print(all_hrefs_list[page_number - 1].get('href'))
