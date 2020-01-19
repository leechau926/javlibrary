from bs4 import BeautifulSoup
import re
import time
import  cloudscraper

scraper = cloudscraper.create_scraper()
scrape_url = 'http://www.javlibrary.com/cn/star_mostfav.php'
web_data = scraper.get(scrape_url).content.decode('utf-8')
soup = BeautifulSoup(web_data, 'lxml')

t_title = soup.find('title').text
print(t_title)

localtime = time.asctime( time.localtime(time.time()) )
print ("本地时间为 :", localtime)

star_list = soup.find_all(name='div', attrs={'class': 'searchitem'})
for star in star_list:
	sequence = star.h3.get_text()
	print(sequence)
	name = star.find(name='img')['title']
	print(name)
	star_id = star['id']
	star_link = 'https://www.javlibrary.com/cn/vl_star.php?s=' + star_id
	print(star_link)
	print('******************************')




