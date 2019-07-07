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


class namuwikiCrawling:

    def __init__(self) -> None:
        super().__init__()

    def start_crawling(self) -> List:

        conn = pymysql.connect(host='localhost', user='root', password='', db='mydb', charset='utf8')
        curs = conn.cursor()


        list_of_idol_group = []
        html = get_html('https://namu.wiki/w/%ED%95%9C%EA%B5%AD%20%EC%95%84%EC%9D%B4%EB%8F%8C/%EB%AA%A9%EB%A1%9D')
        soup = BeautifulSoup(html, 'html.parser')

        # 그룹명 모두 크롤링
        group_names = \
            soup.select("body > div.content-wrapper > article > div.wiki-content.clearfix > div > div > ul > li > ul > li > div > a.wiki-link-internal")
        for group_name in group_names:
            list_of_idol_group = group_name.text
            sql = "INSERT INTO celebrity_group (name, pic_url) VALUES (%s, %s)"
            curs.execute(sql, (group_name.text, ""))
            conn.commit()

        print(len(group_names))







        # 그룹명의 링크를 타고 들어가, 그룹 사진의 url을 저장
        driver = webdriver.Chrome("/Applications/chromedriver")
        driver.implicitly_wait(3)
        driver.get("https://namu.wiki/w/%ED%95%9C%EA%B5%AD%20%EC%95%84%EC%9D%B4%EB%8F%8C/%EB%AA%A9%EB%A1%9D")
        # group_lists = \
        #     driver.find_elements_by_css_selector("body > div.content-wrapper > article > div.wiki-content.clearfix > div > div > ul > li > ul > li > div > a.wiki-link-internal")

        # print(len(group_lists))
        #
        # try {
        #     WebElement group_lists =
        #     driver.find_elements_by_css_selector("body > div.content-wrapper > article > div.wiki-content.clearfix > div > div > ul > li > ul > li > div > a.wiki-link-internal")
        #
        #     for group in group_lists:
        #         driver.get(group.get_attribute('href'))
        #     }
        # catch(org.openqa.selenium.StaleElementReferenceException ex)
        # {
        #     WebElement
        # date = driver.findElement(By.linkText(Utility.getSheetData(path, 7, 1, 2)));
        # date.click();
        # }

        #
        # for group in group_lists:
        #     driver.get(group.get_attribute('href'))





        conn.close()


        return list_of_idol_group

if __name__ == '__main__':
    namuwikiCrawling.start_crawling(namuwikiCrawling)
