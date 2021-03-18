import re

import requests

from bs4 import BeautifulSoup

word = input()
url_link = input()

# word = 'Solomon'
# url_link = 'https://stepik.org/media/attachments/lesson/372811/3._The_Gift_of_the_Magi.shtml'

r = requests.get(url_link, headers={'Accept-Language': 'en-US,en;q=0.5'})
soup = BeautifulSoup(r.content, "html.parser")
paragraphs = soup.find('p', text=re.compile(f'.*{word}.*'))
print(paragraphs.text)
