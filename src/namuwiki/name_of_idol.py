import requests
import pymysql
from typing import List
from bs4 import BeautifulSoup #html을 파싱해주는 라이브러리
from selenium import webdriver


def get_html(url):
    html = ""
    resp = requests.get(url)

    if resp.status_code == 200:
        html = resp.text

    return html


def find_groups_info(driver, conn, curs, list_of_idol_group):


    for idol_group in list_of_idol_group:

        print(idol_group)
        driver.get("https://people.search.naver.com//")

        try:
            search_box = driver.find_element_by_name("query")
            search_box.send_keys(idol_group)
            search_box.submit()
            driver.implicitly_wait(3)

            profile = driver.find_element_by_xpath('//*[@class="who"]//a').get_attribute('href')
            driver.get(profile)




            try:
                group_image = driver.find_element_by_xpath('//*[@class="thmb_img"]').get_attribute('src')
                sql = "INSERT INTO celebrity_group (name, pic_url) VALUES (%s, %s)"
                curs.execute(sql, (idol_group, group_image))
                conn.commit()

            except:
                print("[예외발생]" + idol_group + "이미지 없음")
                sql = "INSERT INTO celebrity_group (name, pic_url) VALUES (%s, %s)"
                curs.execute(sql, (idol_group, ""))
                conn.commit()
                continue

        except:
            print("[예외발생]" + idol_group + "아이돌 없음")
            continue


    curs.close()


# def find_member_info(driver, conn, curs, idol_group):


class namuwikiCrawling:

    def __init__(self) -> None:
        super().__init__()

    def start_crawling(self):

        conn = pymysql.connect(host='localhost', user='root', password='', db='mydb', charset='utf8')
        curs = conn.cursor()


        list_of_idol_group = []

        group_data = []
        member_data = []
        profile_results = []

        html = get_html('https://namu.wiki/w/%ED%95%9C%EA%B5%AD%20%EC%95%84%EC%9D%B4%EB%8F%8C/%EB%AA%A9%EB%A1%9D')
        soup = BeautifulSoup(html, 'html.parser')

        # 그룹명 모두 크롤링
        group_names = \
            soup.select("body > div.content-wrapper > article > div.wiki-content.clearfix > div > div > ul > li > ul > li > div > a.wiki-link-internal")
        for group_name in group_names:
            list_of_idol_group.append(group_name.text)




        print(len(group_names))

        # 그룹명으로 네이버에 검색하여 크롤링
        driver = webdriver.Chrome("/Applications/chromedriver")
        driver.implicitly_wait(3)


        find_groups_info(driver,conn, curs, list_of_idol_group)



        # conn.close()




if __name__ == '__main__':
    namuwikiCrawling.start_crawling(namuwikiCrawling)
