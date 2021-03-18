import requests

from bs4 import BeautifulSoup

index_subtitle = int(input())
url_link = input()

r = requests.get(url_link, headers={'Accept-Language': 'en-US,en;q=0.5'})
soup = BeautifulSoup(r.content, 'html.parser')
all_h2_tags = soup.find_all('h2')

print(all_h2_tags[index_subtitle].text)
