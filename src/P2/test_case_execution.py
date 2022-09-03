# -*- coding: utf-8 -*-
'''
This code is implemented based on a SkillExplorer-like tool called Vitas (you can access Vitas from Github Links here: https://vitas000.github.io/tool/)
'''

import os
from selenium import webdriver
import pickle
import time
import selenium.common
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas
import echo_spider
import argparse
import openpyxl


CHROME_PATH = '../../library/chromedriver'
COOKIE_DIR = '../../cookies/'
LOGOUT_URL = "https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_AccountFlyout_signout%26signIn%3D1%26useRedirectOnSuccess%3D1"

class Spider:
    def __init__(self, cookie_path, password, username, console_url, path):
        options = Options()
        # run program on server
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')
        options.add_argument('use-fake-ui-for-media-stream')

        self.web_driver = webdriver.Chrome(executable_path=path, chrome_options=options)
        self.password = password
        self.username = username
        self.url = console_url
        self.home_page = 'https://www.amazon.com/'
        self.cookie = cookie_path

        if not os.path.exists(cookie_path):
            self.generate_cookie()

        cookie_file = open(cookie_path, 'rb')
        self.cookie_list = pickle.load(cookie_file)
        cookie_file.close()


    def refresh(self):
        self.web_driver.get(self.home_page)
        self.judge_curUrl()
        deviceLevel_element = self.web_driver.find_element("id",'deviceLevel-label')
        self.web_driver.execute_script("arguments[0].click();", deviceLevel_element)
        time.sleep(1)

    def load_cookie(self):
        for cookie in self.cookie_list:
            self.web_driver.add_cookie(cookie)
        time.sleep(2)
        self.web_driver.refresh()
        time.sleep(3)

    def dump_cookie(self):
        new_cookies = self.web_driver.get_cookies()
        cookie1 = {}
        cookie2 = {}
        cookie3 = {}
        cookie4 = {}
        for cookie_tmp in new_cookies:
            if cookie_tmp['name'] == 'ubid-main':
                cookie1['name'] = cookie_tmp['name']
                cookie1['value'] = cookie_tmp['value']
            elif cookie_tmp['name'] == 'x-main':
                cookie2['name'] = cookie_tmp['name']
                cookie2['value'] = cookie_tmp['value']
            elif cookie_tmp['name'] == 'at-main':
                cookie3['name'] = cookie_tmp['name']
                cookie3['value'] = cookie_tmp['value']
            elif cookie_tmp['name'] == 'sess-at-main':
                cookie4['name'] = cookie_tmp['name']
                cookie4['value'] = cookie_tmp['value']
        new_cookies = [cookie1, cookie2, cookie3, cookie4]
        cookie_file = open(self.cookie, 'wb')
        pickle.dump(new_cookies, cookie_file)
        cookie_file.close()

    def auto_login_bak(self):
        try:
            log_in_button = self.web_driver.find_element("xpath",'//*[@id="nav-link-accountList"]')
            self.web_driver.execute_script("arguments[0].click()", log_in_button)
            self.load_cookie()
            self.web_driver.find_element("id",'ap_password').send_keys(self.password)
            self.web_driver.find_element("id",'ap_password').send_keys(Keys.ENTER)
        except selenium.common.exceptions.NoSuchElementException:
            return

    def auto_login(self):
        try:
            self.web_driver.find_element("id",'ap_email').send_keys(self.username)
            self.web_driver.find_element("id",'ap_email').send_keys(Keys.ENTER)
            time.sleep(5)
            self.web_driver.find_element("id",'ap_password').send_keys(self.password)
            self.web_driver.find_element("id",'ap_password').send_keys(Keys.ENTER)
        except selenium.common.exceptions.NoSuchElementException:
            return

    def auto_login_2(self):
        try:
            self.web_driver.find_element("id",'ap_email').send_keys(self.username)
            self.web_driver.find_element("id",'ap_email').send_keys(Keys.ENTER)
            time.sleep(5)
            self.web_driver.find_element("id",'ap_password').send_keys(self.password)
            rem = self.web_driver.find_element("xpath",
                '//*[@id="authportal-main-section"]/div[2]/div/div/div/form/div/div[2]/div/div/label/div/label/input')
            self.web_driver.execute_script("arguments[0].click()", rem)
            self.web_driver.find_element("id",'ap_password').send_keys(Keys.ENTER)
        except selenium.common.exceptions.NoSuchElementException:
            return

    def judge_curUrl(self):
        if self.web_driver.current_url != self.home_page:
            self.web_driver.get(self.home_page)
        time_tmp = time.time()
        while time.time() - time_tmp < 1*60:
            try:
                self.load_cookie()
                break
            except selenium.common.exceptions.InvalidCookieDomainException:
                self.web_driver.get(self.home_page)
                self.web_driver.refresh()
                time.sleep(3)
        self.web_driver.get(self.url)
        if self.web_driver.current_url == self.url:
            return
        self.web_driver.get(LOGOUT_URL)
        self.auto_login()
        self.dump_cookie()
        self.web_driver.get(self.url)
        time.sleep(5)
        if self.web_driver.current_url == self.url:
            return False
        return True

    def open_log_page(self):
        self.judge_curUrl()
        time.sleep(3)
        deviceLevel_element = self.web_driver.find_element("id",'deviceLevel-label')
        self.web_driver.execute_script("arguments[0].click()", deviceLevel_element)
        time.sleep(1)


    def generate_cookie(self):
        if os.path.exists(self.cookie):
            return
        self.web_driver.get(self.home_page)
        log_in_button = self.web_driver.find_element("xpath",'//*[@id="nav-link-accountList"]')
        self.web_driver.execute_script("arguments[0].click()", log_in_button)
        time.sleep(2)
        self.web_driver.find_element("id",'ap_email').send_keys(self.username)
        self.web_driver.find_element("id",'ap_email').send_keys(Keys.ENTER)
        time.sleep(2)
        self.web_driver.find_element("id",'ap_password').send_keys(self.password)
        self.web_driver.find_element("id",'ap_password').send_keys(Keys.ENTER)
        a = input("enter any character to generate_cookie:")
        self.dump_cookie()

    def if_login(self, url):
        self.url = url
        self.web_driver.get(self.url)
        if self.url != self.web_driver.current_url:
            return False
        time.sleep(5)
        source = self.web_driver.page_source
        log_info = re.findall(RE_DIC['log_info'], source)
        if self.web_driver.current_url == self.url and log_info and ('Sign in' in log_info[0]):
            self.web_driver.get(LOGOUT_URL)
            time.sleep(3)
            self.auto_login()
            self.dump_cookie()
            self.web_driver.get(self.url)
            time.sleep(5)
            source = self.web_driver.page_source
            log_info = re.findall(RE_DIC['log_info'], source)
            if log_info and ('Sign in' in log_info[0]):
                return False
            return True
        elif self.web_driver.current_url == self.url and not log_info:
            return False
        else:
            return True

# TYPE test cases
def input_TYPES_test_cases(flag):
    if flag == 1:
        input_str = 'Brisbane'
    elif flag == 2:
        input_str = 'I live in Brisbane'
    elif flag == 3:
        input_str = 'Postcode is 04101'
    elif flag == 4:
        input_str = '04101'
    elif flag == 5:
        input_str = 'My birthday is 25th of December'
    elif flag == 6:
        input_str = 'I am 20 years old'
    elif flag == 7:
        input_str = 'My email is xxx@gmail.com'
    elif flag == 8:
        input_str = 'My phone number is 0450419999'
    elif flag == 9:
        input_str = 'My name is James Smith'
    elif flag == 10:
        input_str = 'James Smith'
    elif flag == 11:
        input_str = '0450419999'

    print('Sending TYPES test cases: ' + input_str)
    return input_str

def input_CHILDREN_test_cases(flag):
    if flag == 1:
        input_str = 'I am under 13'
    if flag == 2:
        input_str = 'I am under 17'
    if flag == 3:
        input_str = 'I am 16 years old'
    if flag == 4:
        input_str = 'I am 10 years old'
    if flag == 5:
        input_str = 'Ten years old'
    if flag == 6:
        input_str = 'Sixteen years old'
    if flag == 7:
        input_str = 'I am a child'
    if flag == 8:
        input_str = 'I am a kid'
    if flag == 9:
        input_str = 'I was born on April 1th, 2010'
    if flag == 10:
        input_str = 'I was born on April 1th, 2006'
    if flag == 11:
        input_str = 'April 1th, 2010'
    if flag == 12:
        input_str = 'April 1th, 2006'

    print('Sending CHILDREN test cases: ' + input_str)
    return input_str

def input_REGIONS_test_cases_Part1(flag):
    if flag == 1:
        input_str = 'I live in California'
    if flag == 2:
        input_str = 'I am resident of California'
    if flag == 3:
        input_str = 'California state'
    if flag == 4:
        input_str = 'I am from California'
    if flag == 5:
        input_str = 'I live in California'
    if flag == 6:
        input_str = 'I am resident of California'
    if flag == 7:
        input_str = 'California state'
    if flag == 8:
        input_str = 'I am from California'

    print('Sending REGIONS test cases: ' + input_str)
    return input_str

def input_REGIONS_test_cases_Part2(flag):
    if flag == 1:
        input_str = 'delete my information'
    if flag == 2:
        input_str = 'erase my information'
    if flag == 3:
        input_str = 'remove my information'
    if flag == 4:
        input_str = 'delete personal information'
    if flag == 5:
        input_str = 'erase personal information'
    if flag == 6:
        input_str = 'remove personal information'
    if flag == 7:
        input_str = 'delete my data'
    if flag == 8:
        input_str = 'erase my data'
    if flag == 9:
        input_str = 'remove my data'

    print('Sending REGIONS test cases: ' + input_str)
    return input_str

def getArgsCategory():
    parser = argparse.ArgumentParser(description='enter the CATEGORY of test cases you want to send')
    parser.add_argument('--t', type=str, help='execute test cases in TYPE category')
    parser.add_argument('--c', type=str, help='execute test cases in CHILDREN category')
    parser.add_argument('--r', type=str, help='execute test cases in REGIONS category')
    args = parser.parse_args()
    if args.t is not None:
        return 'TYPES'
    elif args.c is not None:
        return 'CHILDREN'
    elif args.r is not None:
        return 'REGIONS'

if __name__ == '__main__':
    if not os.path.exists(COOKIE_DIR):
        os.makedirs(COOKIE_DIR)
    cookie = os.path.join(COOKIE_DIR, 'console_cookie7.pkl')
    CONSOLE_URL = 'https://developer.amazon.com/alexa/console/ask/test/amzn1.ask.skill.25a15e7d-7c87-4362-9e32-6f5de7062ef5/development/en_US/#'
    filePath = '../../dataset/SkillExplorer_log'
    testCaseCategory = getArgsCategory()

    # open web driver
    spider = Spider(cookie, "skilltest123", "lm26eg@163.com", CONSOLE_URL, CHROME_PATH)
    spider.open_log_page()
    print('Successfully login!')

    df = pandas.read_excel('SkillExplorer_example_log.xlsx', engine='openpyxl')
    for i in range(0,10):
        dir = df._get_value(i,'Name')
        print('Reading SkillExplorer logs: '+ str(dir))
        text_list = []
        input_list = []
        for file in os.listdir(filePath+'/'+dir):
            if file.endswith(".txt"):
                with open(filePath+'/'+dir+'/'+file) as file:
                    lines = file.readlines()
                    lines = [line.rstrip() for line in lines]
                    text_list.append(lines)

        if len(text_list) == 1:
            continue
        max_list = max(text_list, key=len)
        if len(max_list) < 12:
            continue
        else:
            input_list.append(max_list[0])
            if max_list[2].startswith('alexa open'):
                input_list.append(max_list[4])
            else:
                input_list.append(max_list[2])
            print(input_list)

            if testCaseCategory == 'TYPES':
                testCaseTypeCount = 1
                echo_spider.just_input(spider, 'stop')
                for i in input_list:
                    echo_spider.just_input(spider, i)
                while testCaseTypeCount < 12:
                    echo_spider.just_input(spider, input_TYPES_test_cases(testCaseTypeCount))
                    echo_spider.just_input(spider, 'stop')
                    for i in input_list:
                        echo_spider.just_input(spider, i)
                    testCaseTypeCount += 1

                text = spider.web_driver.find_elements("class name", 'askt-dialog__bubble')
                print('Behavior log: ')
                for t in text:
                    print(t.text)
                spider.web_driver.refresh()


            elif testCaseCategory == 'CHILDREN':
                testCaseChildrenCount = 1
                while testCaseChildrenCount < 13:
                    testCaseTypeCount = 1
                    echo_spider.just_input(spider, 'stop')
                    for i in input_list:
                        echo_spider.just_input(spider, i)
                    while testCaseTypeCount < 12:
                        echo_spider.just_input(spider, input_CHILDREN_test_cases(testCaseChildrenCount))
                        echo_spider.just_input(spider, input_TYPES_test_cases(testCaseTypeCount))
                        echo_spider.just_input(spider, 'stop')
                        for i in input_list:
                            echo_spider.just_input(spider, i)
                        testCaseTypeCount += 1
                    testCaseChildrenCount += 1

                    text = spider.web_driver.find_elements("class name", 'askt-dialog__bubble')
                    print('Behavior log: ')
                    for t in text:
                        print(t.text)
                    spider.web_driver.refresh()


            elif testCaseCategory == 'REGIONS':
                testCaseRegionsCount1 = 1
                testCaseRegionsCount2 = 1
                while testCaseRegionsCount1 < 9:
                    while testCaseRegionsCount2 < 10:
                        testCaseTypeCount = 1
                        echo_spider.just_input(spider, 'stop')
                        for i in input_list:
                            echo_spider.just_input(spider, i)
                        while testCaseTypeCount < 12:
                            echo_spider.just_input(spider, input_TYPES_test_cases(testCaseTypeCount))
                            echo_spider.just_input(spider, input_REGIONS_test_cases_Part1(testCaseRegionsCount1))
                            echo_spider.just_input(spider, input_REGIONS_test_cases_Part2(testCaseRegionsCount2))
                            echo_spider.just_input(spider, 'stop')
                            for i in input_list:
                                echo_spider.just_input(spider, i)
                            testCaseTypeCount += 1
                        testCaseRegionsCount2 += 1

                        text = spider.web_driver.find_elements("class name", 'askt-dialog__bubble')
                        print('Behavior log: ')
                        for t in text:
                            print(t.text)
                        spider.web_driver.refresh()

                    testCaseRegionsCount1 += 1





