from sqlalchemy import Column, Integer, String, Float, DateTime, Text

from setting import Engine
from setting import Base

from setting import TimestampMixin
from pprint import pprint


class Company(Base, TimestampMixin):
    """
    Company model
    """

    __tablename__ = 'companies'
    __table_args__ = {
        'comment': 'Company master model'
    }

    company_name = Column('company_name', String(200))
    website = Column('website', String(200))
    code = Column('code', String(200), primary_key=True)
    segment = Column('segment', String(200))
    score = Column('score', Integer)
    growth = Column('growth', Integer)
    profitability = Column('profitability', Integer)
    stability = Column('stability', Integer)
    size = Column('size', Integer)
    underprice = Column('underprice', Integer)
    rise = Column('rise', Integer)
    category = Column('category', String(100))
    feature = Column('feature', Text)
    consolidated_business = Column('consolidated_business', Text)
    current = Column('current', Float)
    market_capitalization = Column('market_capitalization', String(100))
    minimum_purchase_price = Column('minimum_purchase_price', String(100))
    trading_unit = Column('trading_unit', String(100))
    turnover = Column('turnover', String(100))
    volume = Column('volume', String(100))
    estimate_per = Column('estimate_per', String(100))
    pbr = Column('pbr', String(100))
    expected_dividend_yield = Column('expected_dividend_yield', String(100))
    net_assets_per_share = Column('net_assets_per_share', String(100))
    stock_holding_ratio = Column('stock_holding_ratio', String(100))
    year_high = Column('year_high', String(100))
    year_low = Column('year_low', String(100))
    stock_rise_ratio = Column('stock_rise_ratio', String(100))
    macd = Column('macd', String(100))

if __name__ == "__main__":
    Company.__table__.drop(Engine)
    Base.metadata.create_all(bind=Engine, checkfirst=False)

