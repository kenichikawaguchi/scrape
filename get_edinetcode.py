# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from get_driver import get_driver
import os
import shutil
import pandas as pd


def get_edinetcode():
    url = "https://disclosure2.edinet-fsa.go.jp/weee0010.aspx"

    driver = get_driver()

    wait = WebDriverWait(driver=driver, timeout=30)
    driver.get(url)

    wait.until(EC.presence_of_all_elements_located)

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#GridContainerRow_0001 a"))
    )
    driver.execute_script("onDownloadEdinet()")
    time.sleep(30)
    driver.close()

    driver.quit()

def unzip_dlfile():
    dt_now = datetime.datetime.now()
    str_date = str(dt_now)
    str_date = str_date[:10].replace('-', '')
    filename = "Edinetcode_" + str_date + ".zip"
    print(filename)
    shutil.unpack_archive(filename)


def scode_edit(val):
    return val[:4]


def get_edinetlist():
    df = pd.read_csv("EdinetcodeDlInfo.csv", encoding="cp932", usecols=[0, 6, 11],
                    names=('edinet_code', 'name', 'syoken_code'), dtype={"syoken_code": str}, skiprows=2)
    df = df.dropna(how='any', axis=0)
    df_ex = df.copy()
    df_ex["security_code"] = df_ex["syoken_code"].apply(scode_edit)

    df_ex.to_csv("edinetlist.csv", index=False)

if __name__ == '__main__':
    # get_edinetcode()
    unzip_dlfile()
    get_edinetlist()

