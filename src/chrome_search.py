# 구글에서 "알라딘"을 검색하는 프로그램

from selenium import webdriver

path = "/Applications/chromedriver"
driver = webdriver.Chrome(path)
driver.get("https://www.google.com/")
search_box = driver.find_element_by_name("q")
search_box.send_keys("알라딘")
search_box.submit()
