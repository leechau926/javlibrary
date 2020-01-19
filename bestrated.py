from bs4 import BeautifulSoup
import re
import time
import cloudscraper

scraper = cloudscraper.create_scraper()
scrape_url = 'http://www.javlibrary.com/cn/vl_bestrated.php'
web_data = scraper.get(scrape_url).content.decode('utf-8')
soup = BeautifulSoup(web_data, 'lxml')

t_title = soup.find('title').text
print(t_title)

localtime = time.asctime( time.localtime(time.time()) )
print ("本地时间为 :", localtime)

pattern = re.compile('vid_javli')
t_list = soup.find_all(name='div', attrs={'id':pattern})
# print(t_list)
for item in t_list:
	name = item.a['title']
	address = item.a['href'].replace('.', '')
	link = 'http://www.javlibrary.com/cn' + address
	print('name: ' + name)
	print('link: ' + link)
	print('******************************')
