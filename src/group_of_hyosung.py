"""
네이버에서 효성 계열사를 검색한 후, 계열사 list를 뽑아내는 프로그램
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests

class SiteCrawling:
