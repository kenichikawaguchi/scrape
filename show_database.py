import sqlalchemy
from setting import Inspector, session
from company import Company
from pprint import pprint
from sqlalchemy import select


if __name__ == '__main__':
    columns = Inspector.get_columns("companies")
    print(columns)
    print(Company.__table__.c.keys())
    pprint(columns)
    '''
    result = session.query(Company).all()
    for item in result:
        print(item.company_name)
        print(item.website)
        print(item.code)
        print(item.segment)
        print(item.score)
        print(item.growth)
        print(item.profitability)
        print(item.stability)
        print(item.size)
        print(item.underprice)
        print(item.rise)
        print(item.category)
        print(item.feature)
        print(item.consolidated_business)
        print(item.current)
        print(item.market_capitalization)
        print(item.trading_unit)
        print(item.turnover)
        print(item.volume)
        print(item.estimate_per)
        print(item.pbr)
        print(item.expected_dividend_yield)
        print(item.net_assets_per_share)
        print(item.stock_holding_ratio)
        print(item.year_high)
        print(item.year_low)
        print(item.stock_rise_ratio)
        print(item.macd)
    '''
