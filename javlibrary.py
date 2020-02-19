import cloudscraper
from bs4 import BeautifulSoup
import time
import re
import csv

# set proxies
proxies = {"http": "socks5://192.168.2.103:10808",
           "https": "socks5://192.168.2.103:10808"}

def getinfo(url):
    scraper = cloudscraper.create_scraper()
    web_data = scraper.get(url, proxies=proxies).content.decode('utf-8')
    soup = BeautifulSoup(web_data, 'lxml')

    # print video_title
    video_title_area = soup.find(attrs={'id': 'video_title'})
    video_title = video_title_area.find(name='h3').a.get_text()
    # print("video_title: " + video_title)
    # print video_id
    video_id_area = soup.find(attrs={'id': 'video_id'})
    video_id = video_id_area.find(attrs={'class': 'text'}).get_text()
    # print("video_id: " + video_id)
    # print video_imgurl
    video_imgurl = soup.find(attrs={'id': 'video_jacket'}).img['src']
    # print(video_imgurl)
    # print video_date
    video_date_area = soup.find(attrs={'id': 'video_date'})
    video_date = video_date_area.find(attrs={'class': 'text'}).get_text()
    # print("video_date: " + video_date)
    # print video_director
    video_director_area = soup.find(attrs={'id': 'video_director'})
    video_director = video_director_area.find(attrs={'class': 'text'}).get_text().strip()
    # print("video_director: " + video_director)
    # print video_maker
    video_maker_area = soup.find(attrs={'id': 'video_maker'})
    video_maker = video_maker_area.find(attrs={'class': 'text'}).get_text().strip()
    # print("video_maker: " + video_maker)
    # print video_label
    video_label_area = soup.find(attrs={'id': 'video_label'})
    video_label = video_label_area.find(attrs={'class': 'text'}).get_text().strip()
    # print("video_label: " + video_label)
    # print video_review
    video_review_area = soup.find(attrs={'id': 'video_review'})
    video_review_text = video_review_area.find(attrs={'class': 'score'}).get_text().strip()
    review_pattern = re.compile('\d+.\d+')
    if review_pattern.search(video_review_text).group(0):
        video_review = review_pattern.search(video_review_text).group(0)
    else:
        video_review = ''
    # print("video_review: " + video_review.group(0))
    # print video_cast
    video_cast_area = soup.find(attrs={'id': 'video_cast'})
    video_cast = video_cast_area.find(attrs={'class': 'text'}).get_text().strip()
    # print("video_cast: " + video_cast)
    # print video_genres
    video_genres_area = soup.find(attrs={'id': 'video_genres'})
    genres_list = video_genres_area.find_all(attrs={'class': 'genre'})
    video_genres = ""
    for genre in genres_list:
        video_genres = genre.get_text() + ',' + video_genres
    # print("video_genres: " + video_genres)
    video_dict = {
        'video_title': video_title,
        'video_id': video_id,
        'video_imgurl': video_imgurl,
        'video_date': video_date,
        'video_director': video_director,
        'video_maker': video_maker,
        'video_label': video_label,
        'video_review': video_review,
        'video_cast': video_cast,
        'video_genres': video_genres
    }
    return video_dict

def geturls(url):
    scraper = cloudscraper.create_scraper()
    web_data = scraper.get(url, proxies=proxies).content.decode('utf-8')
    soup = BeautifulSoup(web_data, 'lxml')
    pattern = re.compile('vid_javli')
    t_list = soup.find_all(name='div', attrs={'id': pattern})
    url_list = []
    for item in t_list:
        address = item.a['href'].replace('.', '')
        link = 'http://www.javlibrary.com/cn' + address
        url_list.append(link)
    return url_list

def main(page):
    scrape_url = "https://www.javlibrary.com/cn/vl_mostwanted.php?&mode=&page=" + str(page)
    jav_list = geturls(scrape_url)
    javlib = []
    for url in jav_list:
        javlib.append(getinfo(url))
        print("***completed***" + url)
        # print time
        localtime = time.asctime(time.localtime(time.time()))
        print ("本地时间为 :", localtime)
        time.sleep(5)
    # print(javlib)
    header = ['video_title', 'video_id', 'video_imgurl', 'video_date', 'video_director',
              'video_maker', 'video_label', 'video_review', 'video_cast', 'video_genres']
    with open('javlib.csv', 'a', encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, header)
        # f_csv.writeheader()
        f_csv.writerows(javlib)

if __name__ == "__main__":
    for page in range(1, 11):
        localtime = time.asctime(time.localtime(time.time()))
        print("本地时间为 :", localtime)
        print("######## page %d start ########" % page)
        main(page)
        localtime = time.asctime(time.localtime(time.time()))
        print("本地时间为 :", localtime)
        print("######## page %d completed ########" % page)


