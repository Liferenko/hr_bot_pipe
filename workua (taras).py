import os, sys
from selenium import webdriver
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import traceback
ua=UserAgent(verify_ssl=False)

from pipedrive import Pipedrive



USERNAME = input('Input accout email')
PASSWORD = input('Input accout password')
# from urllib.request import urlretrieve

os.system("chcp 65001")

HEADERS={}
#proxies = {'http':  'http://108.59.14.203:13010',
#                   'https':  'https://108.59.14.203:13010'}
proxies = {}


def sending_requests(link):
    print('start grabbing links for work. Please wait...')
    headers = HEADERS.copy()
    idx = 0
    while idx < 9:
        time.sleep(1.5)
        headers['User-Agent'] = ua.random
        try:
            agent = ua.random
            r = requests.get(link, headers=headers, proxies=proxies)
            if r.status_code != 200:
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
    print('Done!')
def analyze_page(url):
    print('start analizing page for work. Please wait...')
    resume_links = []
    idx_page = 1
    if not url.endswith('/'):
        url = url + '/'
    while True:
        current_url = url + '?page=' + str(idx_page)
        page_content = sending_requests(current_url)
        if not page_content:
            err.write('current_url'+'\n')
            print('cant get page {}, skipping'.format(idx_page))
            idx_page += 1
            if TEST_END_PAGE and idx_page == TEST_END_PAGE:
                break
            continue
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
        if TEST_END_PAGE and idx_page == TEST_END_PAGE:
            break
    return resume_links
    print('Done')



pipedrive = Pipedrive(USERNAME, PASSWORD)
print('Pipedrive Login succeed. Keep going')


def getting_data(url):
    print('Start working. Wait for result:')
    chrome_path = "chromedriver.exe"
    login_url = "https://www.work.ua/employer/login/"
    
    number_of_url_element = 0

    browser = webdriver.Chrome(chrome_path)
    browser.get(login_url)
    time.sleep(0.5)

    usrn = "elitrade.ua@gmail.com"
    pswd = "15976328"

    usrn_form = browser.find_element_by_css_selector("input#email.form-control")
    usrn_form.send_keys(usrn)

    pswd_form = browser.find_element_by_css_selector("input#password.form-control")
    pswd_form.send_keys(pswd)

    submit_btn = browser.find_element_by_css_selector("button.btn.btn-default.btn-block")
    submit_btn.click()

    while number_of_url_element <= len(url):

        browser.get(url[number_of_url_element])

        try:
            contact_a = browser.find_element_by_id("showContacts")
            contact_a.click()
            time.sleep(0.3)

            lead_name = browser.find_element_by_css_selector("h1.cut-top").text
            print(lead_name)

            contact_info = browser.find_elements_by_css_selector("dl.dl-horizontal")[1]
            tmp = contact_info.find_elements_by_css_selector("dd")
            lead_phone = tmp[0].text
            lead_email = tmp[1].text

            download = browser.find_element_by_css_selector("a.download-resume")
            download.click()

            print(lead_phone)
            print(lead_email)
            number_of_url_element += 1

            def create_new_person_plus_deal(lead_name, lead_phone, lead_email):
                pipedrive.persons({
                    'name': lead_name,
                    'org_id': 327,
                    'email': lead_email,
                    'phone': lead_phone,
                    '1abdf0adad500f25d3375c625bcc2532c29980cd': 'найден hr_ботом на work.ua'
                }, method='POST')
                print('New person was created')

                pipedrive.deals({
                    'stage_id': 45,
                    'title': lead_name + '|' + lead_phone,
                    'value': 0,
                    'org_id': 327,
                    'status': 'open'
                }, method='POST')
                print('New deal was created')
            create_new_person_plus_deal(lead_name, lead_phone, lead_email)

        except:
            print("Skip this person (already exist). Go next...")
            number_of_url_element += 1

    print('Scrapping is done. Here is %d new person ready to import into CRM' % (number_of_url_element))
    return True



if __name__ == '__main__':
    TEST_END_PAGE = 2
    err = open('err_log.txt','a')
    main_url_to_scrap_urls = 'https://www.work.ua/resumes-kyiv-management-executive/'
    #url = ['https://www.work.ua/resumes/1221010/', ]
    url = analyze_page(main_url_to_scrap_urls)
    if not url:
        print('Url list is empty, something wrong, exit')
        sys.exit()
    print(url)
    print('Total resume urls:{}'.format(len(url)))
    getting_data(url)
    