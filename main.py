# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_driver():
    service = Service(executable_path='/usr/bin/chromedriver')
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    return driver

if __name__ == '__main__':

    url = "https://disclosure2.edinet-fsa.go.jp/weee0010.aspx"

    driver = get_driver()

    wait = WebDriverWait(driver=driver, timeout=30)
    driver.get(url)

    wait.until(EC.presence_of_all_elements_located)

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#GridContainerRow_0001 a"))
    )
    driver.execute_script("onDownloadEdinet()")
    # a_tag = driver.find_element(By.XPATH, "//a[contains(@onclick,'onDownloadEdinet')]")
    # driver.find_element(By.XPATH, "//a[contains(@onclick,'onDownloadEdinet')]").click()
    # print(type(a_tag))
    # print(a_tag)
    # driver.execute_script('onDownloadEdinet(); return false;')
    time.sleep(30)
    driver.close()

    driver.quit()
