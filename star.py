from bs4 import BeautifulSoup
import re
import time
import cloudscraper

def get_star_zuopin(url):
	scraper = cloudscraper.create_scraper()
	web_data = scraper.get(url).content.decode('utf-8')
	soup = BeautifulSoup(web_data, 'lxml')

	t_title = soup.find('title').text
	print(t_title)

	pattern = re.compile('vid_javli')
	t_list = soup.find_all(name='div', attrs={'id':pattern})
	for item in t_list:
		name = item.a['title']
		address = item.a['href'].replace('.', '')
		link = 'http://www.javlibrary.com/cn' + address
		print('name: ' + name)
		print('link: ' + link)
		print('******************************')

def get_star_pagenum(url):
	scraper = cloudscraper.create_scraper()
	web_data = scraper.get(url).content.decode('utf-8')
	soup = BeautifulSoup(web_data, 'lxml')
	page_url = soup.find(name='a', attrs={'class': 'page last'})
	pattern = re.compile('\=(\d+)$')
	page_num = re.findall(pattern, page_url['href'])
	return page_num[0]

def main():
	url = 'https://www.javlibrary.com/cn/vl_star.php?s=oqjq'
	page_num = int(get_star_pagenum(url))
	for i in range(1, page_num+1):
		i_url = url + '&page=' + str(i)
		get_star_zuopin(i_url)
		print('================page %s end=================' % i)

if __name__ == "__main__":
    main()


