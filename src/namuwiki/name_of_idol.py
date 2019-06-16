import requests
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
        list_of_idol_group = []
        html = get_html('https://namu.wiki/w/%ED%95%9C%EA%B5%AD%20%EC%95%84%EC%9D%B4%EB%8F%8C/%EB%AA%A9%EB%A1%9D')
        soup = BeautifulSoup(html, 'html.parser')

        # 그룹명 모두 크롤링
        a = soup.select("body > div.content-wrapper > article > div.wiki-content.clearfix > div > div > ul > li > ul > li > div > a.wiki-link-internal")
        for aa in a:
            print(aa.text)
        return list_of_idol_group

if __name__ == '__main__':
    namuwikiCrawling.start_crawling(namuwikiCrawling)