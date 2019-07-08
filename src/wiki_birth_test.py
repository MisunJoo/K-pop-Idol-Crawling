from selenium import webdriver
from parse import *
from bs4 import BeautifulSoup
import requests

def get_html(url):
    html = ""
    resp = requests.get(url)

    if resp.status_code == 200:
        html = resp.text

    return html


list_of_idol_group = []

html = get_html('https://namu.wiki/w/%ED%95%9C%EA%B5%AD%20%EC%95%84%EC%9D%B4%EB%8F%8C/%EB%AA%A9%EB%A1%9D')
soup = BeautifulSoup(html, 'html.parser')

# 그룹명 모두 크롤링
group_names = \
    soup.select(
        "body > div.content-wrapper > article > div.wiki-content.clearfix > div > div > ul > li > ul > li > div > a.wiki-link-internal")
for group_name in group_names:
    list_of_idol_group.append(group_name.text)


driver = webdriver.Chrome("/Applications/chromedriver")
driver.implicitly_wait(3)

driver.get("https://people.search.naver.com/search.naver?where=nexearch&sm=tab_ppn&query=%ED%86%A0%EB%8B%88%EC%95%88&os=95982&ie=utf8&key=PeopleService")



idol_member_birth_str = driver.find_element_by_xpath('//*[@class="dsc"]/*[contains(text(), "일")]').text
idol_member_birth_str = idol_member_birth_str.replace("음력", "")
sep = ','
idol_member_birth_str = idol_member_birth_str.split(sep, 1)[0]

idol_member_birth_result = parse("{}년 {}월 {}일", idol_member_birth_str)
idol_member_birth = idol_member_birth_result[0] + "-" + idol_member_birth_result[1] + "-" + idol_member_birth_result[2]

print("출생을 뺀 결과는 " + idol_member_birth)


year_result = driver.find_element_by_xpath('.//tr/td/*[@class="wiki-paragraph"]/span//*[contains(text(), "출생")]/ancestor::td/following-sibling::td//*[contains(text(), "년")]').text
year_parse = parse("{}년", year_result)
year = year_parse[0]
print(year)

month_day_result = driver.find_element_by_xpath('.//tr/td/*[@class="wiki-paragraph"]/span//*[contains(text(), "출생")]/ancestor::td/following-sibling::td//*[contains(text(), "월")]').text
month_day_parse = parse("{}월 {}일", month_day_result)
month = month_day_parse[0]
day = month_day_parse[1]
print(month)
print(day)

brithday = year + "-" + month + "-" + day
print(brithday)

driver.get("https://namu.wiki/w/" + "강타")
