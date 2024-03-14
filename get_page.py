import bs4
import traceback
from get_driver import get_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import json

from setting import Engine, session
from company import Company
from sqlalchemy import insert, update
# from sqlalchemy.dialects.sqlite import insert

from get_code_list import get_code_list

from selenium.common.exceptions import TimeoutException
import traceback


INTERVAL_TIME = 2


def upsert_stmt():
    stmt = insert(Company)
    return stmt.on_conflict_do_update(
        index_elements=['code'],
        set_={
            'company_name': stmt.excluded.company_name,
            'website': stmt.excluded.website,
            'segment': stmt.excluded.segment,
            'score': stmt.excluded.score,
            'growth': stmt.excluded.growth,
            'profitability': stmt.excluded.profitability,
            'stability': stmt.excluded.stability,
            'size': stmt.excluded.size,
            'underprice': stmt.excluded.underprice,
            'rises': stmt.excluded.rise,
            'category': stmt.excluded.category,
            'feature': stmt.excluded.feature,
            'consolidated_business': stmt.excluded.consolidated_business,
            'current': stmt.excluded.current,
            'market_capitalization': stmt.excluded.market_capitalization,
            'minimum_purchase_price': stmt.excluded.minimum_purchase_price,
            'trading_unit': stmt.excluded.trading_unit,
            'turnover': stmt.excluded.turnover,
            'volume': stmt.excluded.volume,
            'estimate_per': stmt.excluded.estimate_per,
            'pbr': stmt.excluded.pbr,
            'expected_dividend_yield': stmt.excluded.expected_dividend_yield,
            'net_assets_per_share': stmt.excluded.net_assets_per_share,
            'stock_holding_ratio': stmt.excluded.stock_holding_ratio,
            'year_high': stmt.excluded.year_high,
            'year_low': stmt.excluded.year_low,
            'stock_rise_ratio': stmt.excluded.stock_rise_ratio,
            'macd': stmt.excluded.macd,
            'updated_at': stmt.excluded.updated_at
        }
    )

def get_page(driver, url):
    driver = get_driver()
    try:
        driver.get(url)
        result_exception = 0
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'overview__main__information')))
        page = driver.page_source
    except TimeoutException as e:
        print("TimeoutException")
        result_exception = 1
        page = None
    except Exception as e:
        t = list(traceback.TracebackException.from_exception(e).format())
        print(t)
        result_exception = 1
        page = None


    return page, result_exception


def refine_text(text):
    return str.strip(text.replace('\n', ''))


def refine_number(text):
    tmp = refine_text(text)
    tmp = tmp.replace('円', '')
    tmp = tmp.replace(',', '')
    try:
        result = float(tmp)
    except ValueError:
        result = float(-1)
    return result


def get_key_value_from_stock(spans):
    sub_spans = spans[1].find_all("span")
    if refine_text(spans[0].text) == "予想PER":
        if len(sub_spans) == 0:
            return "-", "-"
        if len(sub_spans) == 1:
            return refine_text(spans[0].text), "-"
        if len(sub_spans) == 2:
            return refine_text(spans[0].text), refine_text(spans[1].text)
        return refine_text(spans[0].text), refine_text(sub_spans[2].text)
    elif refine_text(spans[0].text) == "予想配当利回り":
        if len(sub_spans) == 0:
            return "-", "-"
        if len(sub_spans) == 1:
            return refine_text(spans[0].text), "-"
        if len(sub_spans) == 2:
            return refine_text(spans[0].text), refine_text(spans[1].text)
        return refine_text(spans[0].text), refine_text(sub_spans[2].text)
    elif refine_text(spans[0].text) == "1株純資産":
        if len(sub_spans) == 0:
            return "-", "-"
        if len(sub_spans) == 1:
            return refine_text(spans[0].text), "-"
        if len(sub_spans) == 2:
            return refine_text(spans[0].text), refine_text(spans[1].text)
        return refine_text(spans[0].text), refine_text(sub_spans[2].text)
    else:
        return refine_text(spans[0].text), refine_text(spans[1].text)


def get_data_from_page(page):
    soup = bs4.BeautifulSoup(page, features='lxml')
    try:
        information = {}
        current = None

        main_elem = soup.find("div", class_="main")
        if main_elem:
            name_elem = main_elem.find("h1")
            if name_elem:
                information['company_name'] = name_elem.text

        hp = soup.find("div", class_="information__top__hp")
        if hasattr(hp, 'find'):
            if hp.find("a"):
                if hp.find("a").get("href"):
                    information["website"] = refine_text(hp.find("a").get("href"))
                else:
                    information["website"] = '-'
            else:
                information["website"] = '-'
        else:
            information["website"] = '-'

        information_elem = soup.find("div", class_="information")
        company_code = refine_text(soup.find("span", class_="head__top__item__code").text)
        company_class = refine_text(soup.find("span", class_="head__top__item__name").text)
        information['code'] = company_code
        information['segment'] = company_class
        stars = soup.find("div", class_="score__head").find("span")
        if stars.text.isdigit():
            score = int(stars.text)
        else:
            score = -1

        information['score'] = score

        score_chart = soup.find_all("div", class_="score__chart-wrapper__main__list")
        dtdd_all = score_chart[0].find_all(["dt", "dd"]) + score_chart[1].find_all(["dt", "dd"])

        for dtdd in dtdd_all:
            if dtdd.name == "dt":
                dt_tag = refine_text(dtdd.text)
            else:
                dd_tag = refine_text(dtdd.text)
                if dt_tag == '成長性':
                    key = 'growth'
                elif dt_tag == '収益性':
                    key = 'profitability'
                elif dt_tag == '安全性':
                    key = 'stability'
                elif dt_tag == '規模':
                    key = 'size'
                elif dt_tag == '割安度':
                    key = 'underprice'
                elif dt_tag == '値上がり':
                    key = 'rise'
                else:
                    key = dt_tag
                if dd_tag.isdigit():
                    information[key] = int(dd_tag)
                else:
                    information[key] = -1

        category = soup.find("div", class_="score__chart-wrapper__note")
        if hasattr(category, 'contents'):
            category = category.contents[0].replace("業種：", "")
        else:
            category = '-'

        information["category"] = refine_text(category)

        information_list = information_elem.find("dl", class_="information__list")
        if information_list:
            dtdd_tag_all = information_list.find_all(["dt","dd"])
            dt_tag = ""
            dd_tag = ""
            for dtdd in dtdd_tag_all:
                if dtdd.name == "dt":
                    dt_tag = refine_text(dtdd.text)
                else:
                    dd_tag = refine_text(dtdd.text)

                if len(dt_tag) > 0 and len(dd_tag) > 0:
                    if dt_tag == '特色':
                        key = 'feature'
                    elif dt_tag == '連結事業':
                        key = 'consolidated_business'
                    else:
                        key = dt_tag

                    information[key] = dd_tag
                    dt_tag = ""
                    dd_tag = ""

        rival = []
        rival_list = soup.find("div", class_="rivals__items")
        if rival_list:
            rival_all = rival_list.find_all("div", class_='rivals__items__item')
            for rival_ in rival_all:
                spans = rival_.find_all("span")
                tmp_company = {"code": refine_text(spans[0].text),
                                "name": refine_text(spans[1].text)}
                rival.append(tmp_company)

        current_elem = soup.find("div", class_="stock-index__price__current")
        if current_elem:
            current = refine_number(current_elem.text)

        section_elem = soup.find("div", class_="basic-section")
        if section_elem:
            stock = {}
            li_tag_all = section_elem.find(class_="stock-index").find_all("li")
            for li_tag in li_tag_all:
                spans = li_tag.find_all("span")
                key, value = get_key_value_from_stock(spans)
                if key == '時価総額':
                    key = 'market_capitalization'
                elif key == '最低購入金額':
                    key = 'minimum_purchase_price'
                elif key == '売買単位':
                    key = 'trading_unit'
                elif key == '売買代金':
                    key = 'turnover'
                elif key == '出来高':
                    key = 'volume'
                elif key == '予想PER':
                    key = 'estimate_per'
                elif key == '実績PBR':
                    key = 'pbr'
                elif key == '予想配当利回り':
                    key = 'expected_dividend_yield'
                elif key == '1株純資産':
                    key = 'net_assets_per_share'
                elif key == '自己株保有率':
                    key = 'stock_holding_ratio'
                elif key == '年初来高値':
                    key = 'year_high'
                elif key == '年初来安値':
                    key = 'year_low'
                elif key == '年初来株価上昇率':
                    key = 'stock_rise_ratio'
                elif key == '200日移動平均乖離率':
                    key = 'macd'
                elif '22日平均' in key:
                    continue
                elif '実績PER' in key:
                    continue

                stock[key] = value
                #stock[refine_text(spans[0].text)] = refine_text(spans[1].text)

        rivals = {"rival": rival}
        data = dict(**information, **{"current": current}, **stock)

        info = {
                "information": information,
                "rival": rival,
                "current": current,
                "stock": stock
               }

        return data, rivals

    except Exception as e:
        print("Exception\n" + traceback.format_exc())
        return None


if __name__ == "__main__":

    code_list = get_code_list()
    base_url = "https://shikiho.jp/stocks/"

    driver = get_driver()

    page_counter = 0
    data = []

    #session.query(Company).delete()

    for index, code in enumerate(code_list):
        page_counter = page_counter + 1
        target_url = base_url + str(code) + "/"
        page_result = get_page(driver, target_url)
        page = page_result[0]
        page_error = page_result[1]
        if page_error == 1:
            print(str(index), str(code), "ERROR")
            time.sleep(INTERVAL_TIME)
            continue
        result = get_data_from_page(page)
        company_data = result[0]
        rivals = result[1]

        data.append(company_data)
        print(str(index), str(code),
            company_data['company_name'],
            "業種: ",
            company_data['category'],
            "株価: ",
            company_data['current'],
            "特色: ",
            company_data['feature']
        )

        res = session.query(Company).filter(Company.code == code).first()
        if res:
            print(str(index) + ' ' + str(code) + ' is found.')
            session.execute(update(Company),company_data)
        else:
            print(str(index) + ' ' + str(code) + ' is NOT found.')
            session.execute(insert(Company),company_data)

        #session.commit()

        # session.execute(clause=upsert_stmt(),params=company_data)
        session.commit()

        time.sleep(INTERVAL_TIME)

    print(json.dumps(data, indent=2, ensure_ascii=False))
    with open('dump.json', 'wt') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


    driver.quit()

    session.close()
