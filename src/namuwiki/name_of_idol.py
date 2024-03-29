import requests
import pymysql
from typing import List
from parse import *
from bs4 import BeautifulSoup  # html을 파싱해주는 라이브러리
from selenium import webdriver

def namuwiki_birthday(idol_member_name, driver):
    if(idol_member_name.find("(")):
        idol_member_name_result = idol_member_name.split('(')[0]
    else:
        idol_member_name_result = idol_member_name

    idol_member_name_result = idol_member_name_result.replace("음력", "")

    driver.get("https://namu.wiki/w/" + idol_member_name_result)

    try:

        year_result = driver.find_element_by_xpath(
            './/tr/td/*[@class="wiki-paragraph"]//*[contains(text(), "출생")]/ancestor::td/following-sibling::td//*[contains(text(), "년")]').text

        if 'year_result' in locals():

            year_parse = parse("{}년", year_result)
            year = year_parse[0]

            month_day_result = driver.find_element_by_xpath(
                './/tr/td/*[@class="wiki-paragraph"]//*[contains(text(), "출생")]/ancestor::td/following-sibling::td//*[contains(text(), "월")]').text
            month_day_parse = parse("{}월 {}일", month_day_result)
            month = month_day_parse[0]

            day = month_day_parse[1]

            birthday = year + "-" + month + "-" + day
        return birthday

    except Exception as e:
            year = str(1900)
            month = str(10)
            day = str(10)
            birthday = year + "-" + month + "-" + day

            return birthday


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

        # try:
        search_box = driver.find_element_by_name("query")
        search_box.send_keys(idol_group)
        search_box.submit()
        driver.implicitly_wait(3)

        try:
            profile = driver.find_element_by_xpath('//*[@class="who"]//a').get_attribute('href')
            driver.get(profile)
            group_image = driver.find_element_by_xpath('//*[@class="thmb_img"]').get_attribute('src')
            sql = "INSERT INTO celebrity_group (name, pic_url) VALUES (%s, %s)"
            curs.execute(sql, (idol_group, group_image))
            conn.commit()

            sql = "SELECT id FROM celebrity_group WHERE name = %s"
            curs.execute(sql, (idol_group,))
            idol_id = curs.fetchone()

            print(idol_id)
            find_member_info(driver, conn, curs, idol_group, idol_id)

        except Exception as e:
            print(e)
            print("[예외발생]" + idol_group + "이미지 없음")
            sql = "INSERT INTO celebrity_group (name, pic_url) VALUES (%s, %s)"
            curs.execute(sql, (idol_group, ""))
            conn.commit()

            sql = "SELECT id FROM celebrity_group WHERE name = %s"
            curs.execute(sql, (idol_group,))
            idol_id = curs.fetchone()

            print(idol_id)
            find_member_info(driver, conn, curs, idol_group, idol_id)
            continue

    # except:
    #     print("[예외발생]" + idol_group + "아이돌 없음")
    #     continue


def find_member_info(driver, conn, curs, idol_group, idol_id):
    idol_members = []
    idol_members_xpath = driver.find_elements_by_xpath('//*[@class="dsc"]/dd/*[contains(@href, "people")]')

    for idol_member_path in idol_members_xpath:
        idol_members.append(idol_member_path.get_attribute('href'))

    for idol_member in idol_members:
        driver.get(idol_member)
        idol_member_name = driver.find_element_by_xpath('//*[@class="name"]').text
        idol_member_pic = driver.find_element_by_xpath('//*[@class="thmb_img"]').get_attribute('src')


        try:

            idol_member_birth_str = driver.find_element_by_xpath('//*[@class="dsc"]/*[contains(text(), "일")]').text
            idol_member_birth_str = idol_member_birth_str.replace("음력", "")
            sep = ','
            idol_member_birth_str = idol_member_birth_str.split(sep, 1)[0]

            idol_member_birth_result = parse("{}년 {}월 {}일", idol_member_birth_str)
            idol_member_birth = idol_member_birth_result[0] + "-" + idol_member_birth_result[1] + "-" + \
                                idol_member_birth_result[2]


            sql = "INSERT INTO celebrity_member (name, birthday, pic_url, group_id) VALUES (%s, %s, %s, %s)"
            curs.execute(sql, (idol_member_name, idol_member_birth, idol_member_pic, idol_id))
            conn.commit()


            print(idol_member_birth)
        except Exception as e:
            print(e)
            print("[예외발생]" + idol_member_name + "생일 밝히지 않음")

            idol_member_birth = namuwiki_birthday(idol_member_name, driver)

            sql = "INSERT INTO celebrity_member (name, birthday, pic_url, group_id) VALUES (%s, %s, %s, %s)"

            curs.execute(sql, (idol_member_name, idol_member_birth, idol_member_pic, idol_id))

            conn.commit()





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
            soup.select(
                "body > div.content-wrapper > article > div.wiki-content.clearfix > div > div > ul > li > ul > li > div > a.wiki-link-internal")
        for group_name in group_names:
            list_of_idol_group.append(group_name.text)

        print(len(group_names))

        # 그룹명으로 네이버에 검색하여 크롤링
        driver = webdriver.Chrome("/Applications/chromedriver")
        driver.implicitly_wait(3)

        find_groups_info(driver, conn, curs, list_of_idol_group)

        # conn.close()


if __name__ == '__main__':
    namuwikiCrawling.start_crawling(namuwikiCrawling)
