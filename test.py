import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import re
import time
import sys

"""# Functions"""
def get_links(url):
    data = []
    http = httplib2.Http()
    status, response = http.request(url)
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            data.append(link['href'])
    return data

def get_next_link(data):
    pattern = '/wiki/.'
    for i in data:
        if re.match(pattern, i):
            if (':' not in i) and ('(' not in i):
                if i.split('/')[2] != 'Main_Page':
                    return i

    return -1

def check_target(page):
    if "Philosophy" in page:
        return True



if __name__ == '__main__':
    start_url = '/wiki/Special:Random'
    max_requests = int(sys.argv[1])
    non_stop = sys.argv[2]
    yeild = float(sys.argv[3])
    visited_links = []
    page = start_url
    for i in range(max_requests):
        data = get_links('https://en.wikipedia.org' + page)
        page = get_next_link(data)
        print(page)
        if check_target(page):  # If we reached our target
            break
        elif page in visited_links:  # If cycle
            print("Cycle")
            if non_stop == 'True':
                page = start_url  #For starting again
            else:
                break
        else:
            visited_links.append(page)
            time.sleep(yeild)
