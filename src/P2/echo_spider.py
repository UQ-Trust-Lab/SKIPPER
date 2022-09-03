# -*- coding: utf-8 -*-
'''
This code is implemented based on a SkillExplorer-like tool called Vitas (you can access Vitas from Github Links here: https://vitas000.github.io/tool/)
'''

import time
from selenium.webdriver.common.keys import Keys
import selenium.common

RE_DIC = {
    'log_list': r'<div class="askt-log__list-element (?:"|askt-log__list-element--active") title="(.*?)">',
    'log_item': "//div[@class='askt-log__list-element ' and @title='%s']",
    'log_info_list': r'<div class="ace_line" style="height:(\d+(\.\d+)?)px">(.*?)</div>',
    'log_info_item': r'<span class="ace_string">(.*?)</span>',
    'log_info': r'<span class="nav-line-1">(.*?)</span>'
}

def re_open(spider):
    time_start = time.time()
    time.sleep(0.5)
    while time.time() - time_start <= 10:
        try:
            just_input(spider, 'exit')
            break
        except selenium.common.exceptions.NoSuchElementException:
            continue
    while time.time() - time_start <= 60:
        try:
            spider.judge_curUrl()
        except selenium.common.exceptions.TimeoutException:
            continue
        # open log window
        try:
            deviceLevel_element = spider.web_driver.find_element_by_id('deviceLevel-label')
            spider.web_driver.execute_script("arguments[0].click()", deviceLevel_element)
        except selenium.common.exceptions.NoSuchElementException:
            continue
        return True
    return False


def just_input(spider, input_string):
    search_bar = spider.web_driver.find_element("xpath",'//*[@id="astro-tabs-1-panel-0"]/div[1]/div[2]/div[1]/div[1]/input')
    search_bar.send_keys(input_string)
    time.sleep(1)  # You can skip this.
    search_bar.send_keys(Keys.ENTER)
    time.sleep(4)




