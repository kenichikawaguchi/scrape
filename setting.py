from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime


# 接続先DBの設定
DATABASE = 'sqlite:///db.sqlite3'

# Engine の作成
Engine = create_engine(
  DATABASE,
  echo=False
)
Base = declarative_base()

# Sessionの作成
session = Session(
  autocommit = False,
  autoflush = True,
  bind = Engine
)

# modelで使用する
Base = declarative_base()

class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
        )


Inspector = inspect(Engine)

