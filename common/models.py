from typing import List

from datetime import datetime
from enum import Enum, unique

# use config for each project
from config import BaseConfig
from sqlalchemy import (
    create_engine, Column, String, Integer, DateTime, ForeignKey, Boolean, Text, Date, Time, Float
)

base_config = BaseConfig()

if base_config.APP_NAME == 'WEB':
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy.orm import relationship

    db = SQLAlchemy()
    base = db.Model
else:
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship, scoped_session

    # APP_NAME is one of ['DICOM', 'EXPORT', ...]
    db = create_engine(
        base_config.SQLALCHEMY_DATABASE_URI,
        isolation_level="READ COMMITTED"
    )
    base = declarative_base(db)
    Session = scoped_session(sessionmaker(db))
    session = Session()


class BaseModel(base):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)


class Coin(BaseModel, base):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True)
    coin_name = Column(String(300))

    def __init__(self, coin_name):
        self.coin_name = coin_name


class CoinRecord(BaseModel, base):
    __tablename__ = 'coin_records'

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey("coins.id"))
    trade_price = Column(Float)
    last_updated_at = Column(DateTime)

    def __init__(self, coin_id, trade_price):
        self.coin_id = coin_id
        self.trade_price = trade_price
        self.last_updated_at = datetime.now()


class Alarm(BaseModel, base):
    __tablename__ = 'alarms'

    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey("coins.id"))
    detail_text = Column(Text)
    created_at = Column(DateTime)

    def __init__(self, coin_id, detail_text):
        self.coin_id = coin_id
        self.detail_text = detail_text
        self.created_at = datetime.now()