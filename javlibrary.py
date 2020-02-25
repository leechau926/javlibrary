import cloudscraper
from bs4 import BeautifulSoup
import time
import re
import csv
import os

html_dir = '/root/javlib/jav_html/'
csv_dir = '/root/javlib/jav_csv/'
key_word = 'jul'
search_url = 'https://www.javlibrary.com/cn/vl_searchbyid.php?keyword=%s' % key_word



def get_maxpage(url):
    scraper = cloudscraper.create_scraper()
    web_data = scraper.get(url).content.decode('utf-8')
    soup = BeautifulSoup(web_data, 'lxml')
    page_num_area = soup.find(attrs={'class': 'page last'})
    num_pattern = re.compile('page=(\d+)')
    page_num = re.findall(num_pattern, page_num_area['href'])[0]
    return int(page_num)


def get_urls(url):
    scraper = cloudscraper.create_scraper()
    web_data = scraper.get(url).content.decode('utf-8')
    soup = BeautifulSoup(web_data, 'lxml')
    pattern = re.compile('vid_javli')
    t_list = soup.find_all(name='div', attrs={'id': pattern})
    url_list = []
    for item in t_list:
        address = item.a['href'].replace('.', '')
        link = 'http://www.javlibrary.com/cn' + address
        url_list.append(link)
    return url_list


def get_html(url):
    htmlname_pattern = re.compile('=(\w+)')
    html_name = re.findall(htmlname_pattern, url)[0]
    scraper = cloudscraper.create_scraper()
    web_data = scraper.get(url).content.decode('utf-8')
    soup = BeautifulSoup(web_data, 'lxml')
    video_id_area = soup.find(attrs={'id': 'video_id'})
    video_id = video_id_area.find(attrs={'class': 'text'}).get_text()
    with open(html_dir + video_id + html_name + '.html', 'w', encoding='utf-8') as f:
        f.write(web_data)
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime + ' **** %s html saved ****' % video_id)


def read_html(file):
    f = open(file, 'r', encoding='utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')
    video_title_area = soup.find(attrs={'id': 'video_title'})
    video_title = video_title_area.h3.get_text()
    video_id_area = soup.find(attrs={'id': 'video_id'})
    video_id = video_id_area.find(attrs={'class': 'text'}).get_text()
    video_imgurl = 'https:' + soup.find(attrs={'id': 'video_jacket'}).img['src']
    video_date_area = soup.find(attrs={'id': 'video_date'})
    video_date = video_date_area.find(attrs={'class': 'text'}).get_text()
    video_director_area = soup.find(attrs={'id': 'video_director'})
    video_director = video_director_area.find(attrs={'class': 'text'}).get_text().strip()
    video_maker_area = soup.find(attrs={'id': 'video_maker'})
    video_maker = video_maker_area.find(attrs={'class': 'text'}).get_text().strip()
    video_label_area = soup.find(attrs={'id': 'video_label'})
    video_label = video_label_area.find(attrs={'class': 'text'}).get_text().strip()
    video_review_area = soup.find(attrs={'id': 'video_review'})
    if video_review_area:
        video_review_text = video_review_area.find(attrs={'class': 'score'}).get_text().strip()
        review_pattern = re.compile('\d+.\d+')
        if review_pattern.search(video_review_text):
            video_review = review_pattern.search(video_review_text).group(0)
        else:
            video_review = ''
    else:
        video_review = ''
    video_cast_area = soup.find(attrs={'id': 'video_cast'})
    video_cast = video_cast_area.find(attrs={'class': 'text'}).get_text().strip()
    video_genres_area = soup.find(attrs={'id': 'video_genres'})
    genres_list = video_genres_area.find_all(attrs={'class': 'genre'})
    video_genres = ""
    for genre in genres_list:
        video_genres = genre.get_text() + ',' + video_genres
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


def write_csv(dict):
    headers = ['video_title', 'video_id', 'video_imgurl', 'video_date', 'video_director', 'video_maker',
               'video_label', 'video_review', 'video_cast', 'video_genres']
    with open(csv_dir + key_word + '.csv', 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(dict)


def main(page):
    scrape_url = search_url + "&page=" + str(page)
    jav_list = get_urls(scrape_url)
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime + ' **** In this page there is %d url ****' % len(jav_list))
    for url in jav_list:
        try:
            get_html(url)
        except:
            localtime = time.asctime(time.localtime(time.time()))
            print(localtime + ' **** Error occured, wait for 10 seconds ****')
            time.sleep(10)
            get_html(url)


if __name__ == '__main__':
    page_max = get_maxpage(search_url)
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime + ' **** max page number is %d ****' % page_max)
    for i in range(1, page_max + 1):
        localtime = time.asctime(time.localtime(time.time()))
        print(localtime + " #### page %d start ####" % i)
        main(i)
        localtime = time.asctime(time.localtime(time.time()))
        print(localtime + " #### page %d completed ####" % i)
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime + " #### Saving html completed ####")
    jav_dict = []
    for filename in os.listdir(html_dir):
        jav_dict.append(read_html(html_dir + filename))
    write_csv(jav_dict)

