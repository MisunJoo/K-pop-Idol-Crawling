import requests
from bs4 import BeautifulSoup

req = requests.get('https://www.naver.com/')
source = req.text #req 변수에 저장된 HTML소스를 가져옴
soup = BeautifulSoup(source, 'html.parser')

top_list = soup.select(
    "#PM_ID_ct > div.header > div.section_navbar > div.area_hotkeyword.PM_CL_realtimeKeyword_base > div.ah_list.PM_CL_realtimeKeyword_list_base > ul > li > a.ah_a > span.ah_k")
for top in top_list:
    print(top.text)