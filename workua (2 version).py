import os
from selenium import webdriver
import time
# from urllib.request import urlretrieve

os.system("chcp 65001")

chrome_path = "chromedriver.exe"
login_url = "https://www.work.ua/employer/login/"
url = "https://www.work.ua/resumes/3416419/"

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

browser.get(url)

contact_a = browser.find_element_by_id("showContacts")
contact_a.click()
time.sleep(0.3)

name = browser.find_element_by_css_selector("h1.cut-top").text
print(name)

contact_info = browser.find_elements_by_css_selector("dl.dl-horizontal")[1]
tmp = contact_info.find_elements_by_css_selector("dd")


phone = tmp[0].text
email = tmp[1].text

download = browser.find_element_by_css_selector("a.download-resume")
download.click()

print(phone)
print(email)

exit()

