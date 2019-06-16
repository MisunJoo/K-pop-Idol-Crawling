# -*- coding: utf-8 -*-
# ! /usr/bin/env python3

"""
네이버에서 효성 계열사를 검색한 후, 계열사 list를 뽑아내는 프로그램
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import re
from typing import List
from const import *


class SiteCrawling:

    def __init__(self) -> None:
        super().__init__()

    def start_crawling(self) -> List:
        list_of_company = []

        # 네이버 검색창에서 효성 계열사 검색
        driver = webdriver.Chrome("/Applications/chromedriver")
        driver.implicitly_wait(3)
        driver.get("https://www.naver.com/")
        search_box = driver.find_element_by_id("query")
        search_box.send_keys("효성계열사")
        # search_box.submit()
        search_box.find_element_by_xpath('//*[@id="search_btn"]').click()

        # HTML로부터 데이터를 가져오기 위한 BeautifulSoup 생성
        # 계열사가 전체 몇 페이지인지 가져옴
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        total_page = \
            soup.select(
                '#main_pack > div.sp_company_list.sc._au_company_search._company_list > div.api_subject_bx > div.paging_area._page_navi > div > span.page_number > strong.total._total_page')
        total_page = int(re.sub(r'\D', "", total_page[0].text))

        return list_of_company

a = {"김" : 1,"이" : 2,  }
(1,2,3,4)


#
# if __name__ == '__main__':
#     SiteCrawling.start_crawling()
# ???? 왜 이건 에러가 나지??
# TypeError: start_crawling() missing 1 required positional argument: 'self'

# if __name__ == '__main__':
#     SiteCrawling().start_crawling()

if __name__ == '__main__':
    SiteCrawling.start_crawling()
