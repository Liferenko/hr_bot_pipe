#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import traceback
ua=UserAgent(verify_ssl=False)

HEADERS={}
proxies = {'http':  'http://108.59.14.203:13010',
                   'https':  'https://108.59.14.203:13010'}
def sending_requests(link):
    headers = HEADERS.copy()
    idx = 0
    while idx < 9:
        headers['User-Agent'] = ua.random
        try:
            agent = ua.random
            r = requests.get(link, headers=headers, proxies=proxies)
            if r.status_code != 200:# or :
                print('Status code: {}\n{}'.format(r.status_code, link))
            if r.status_code == 200:
                print('Success! {}'.format(link))
                return r.text
        except:
            idx += 1
        idx+=1
    else:
        traceback.print_exc()
        return False
        
def analyze_page(url):
    resume_links = []
    idx_page = 1
    if not url.endswith('/'):
        url = url + '/'
    while True:
        current_url = url + '?page=' + str(idx_page)
        page_content = sending_requests(current_url)
        if not page_content:
            err.write('current_url'+'\n')
        source = BeautifulSoup(page_content, 'lxml')
        cards = source.findAll('div',{'class':'resume-link'})
        if not cards:
            break
        for card in cards:
            link = [a['href'] for a in card.findAll('a',{'href':True}) if '/resumes/' in a['href']]
            if not link:
                continue
            link = link[0]
            if not link.startswith('https://www.work.ua'):
                link = 'https://www.work.ua' + link
            resume_links.append(link)
        idx_page += 1
    return resume_links
    
if __name__ == '__main__':
    err = open('err_log.txt','a')
    url = 'https://www.work.ua/resumes-kyiv-management-executive/'
    
    links = analyze_page(url)