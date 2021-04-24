# This script is used to crawl swami vivekannad's writings from nltr.org 
import pickle
from os import makedirs, path, remove
from shutil import rmtree
from urllib.request import urlopen
from bs4 import BeautifulSoup

# A dictionary of type {int: [String]} in which
#  key represents khanda_number and
#  value represents already cralled page's urls
already_crawlled = {}
links_db_path = 'links-db'
data_root_path = 'data'

# Crawls text from page specified by the URL
# Returns a tuple containing (text, next_page_url)
# If there is no next page, next_page_url shall be empty
def crawl(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    normal_txt = ''.join(list(map(lambda x: x.text, soup.find_all('p', attrs={'class' : 'normal1'}))))
    right_nav =  fech_right_navigation(soup)
    return (normal_txt, right_nav)

def fech_right_navigation(soup):
    right_navigation = soup.find('div', {'id': 'rightnavigation'})
    if right_navigation and right_navigation.a:
        next_page_link = right_navigation.a['href']
        return 'https://baniorachana.nltr.org/' + next_page_link
    return None
    
# Remove data directory from disk
def clear_data():
    # Delete existing data
    # Delete links-db 
    if path.exists(data_root_path):
        rmtree(data_root_path)
    if path.exists(links_db_path):
        remove(links_db_path)

def load_intial_links():
    global already_crawlled
    already_crawlled = {}

    with open('starting-links', 'r') as fp:
        url_list = fp.readlines()
        for (idx, url) in enumerate(url_list):
            already_crawlled[idx + 1] = [url]

def load_links_from_db():
    if not path.exists(links_db_path):
        load_intial_links()
        write_to_db()
        return

    global already_crawlled
    with open(links_db_path, 'rb') as db:
        already_crawlled = pickle.load(db)

def write_to_db():
    with open(links_db_path, 'wb') as db:
        pickle.dump(already_crawlled, db, pickle.HIGHEST_PROTOCOL)

def write_text(khanda_number, page_number, text):
    file_dir = '{}/khanda-{}'.format(data_root_path, khanda_number)
    makedirs(file_dir, exist_ok=True)
    file_path = file_dir + '/khanda-{}__page-{}.txt'.format(khanda_number, page_number)
    with open(file_path, 'w') as fp:
        fp.write(text)

def start():
    load_links_from_db()
    for khanda_number in already_crawlled.keys():
        url_list = already_crawlled[khanda_number]
        # For code simplicity crawll last crawlled page again
        # Otherwise we have to check many things, we don't need
        # to take that much overhead
        last_url = url_list[-1]        
        while True:
            page_number = len(url_list)
            print("Khanda {}, Page {}, URL: {}".format(khanda_number, page_number, last_url))
            text, next_url = crawl(last_url)
            write_text(khanda_number, page_number, text)
            if not next_url:
                break
            url_list.append(next_url)
            last_url = next_url
            write_to_db()
