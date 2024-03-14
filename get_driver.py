# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_driver():
    service = Service(executable_path='/usr/bin/chromedriver')
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    return driver
