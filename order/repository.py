from dataclasses import dataclass
from datetime import date, datetime
from typing import List

from pandas import DataFrame
from sqlalchemy import Column, Text, Float, Integer, Date, DateTime
from sqlalchemy.dialects.postgresql import insert

from ddd import ValueObject
from rdb import RdbEntity
from rdb.session import RdbSession


@dataclass(frozen=True)
class OrderDataFrame(ValueObject):
    data_frame: DataFrame


class _Order(RdbEntity):
    __tablename__ = "ibkr_orders"
    ibOrderID = Column(Text, primary_key=True)
    accountId = Column(Text)
    acctAlias = Column(Text)
    model = Column(Text)
    currency = Column(Text)
    fxRateToBase = Column(Float)
    assetCategory = Column(Text)
    symbol = Column(Text)
    description = Column(Text)
    conid = Column(Integer)
    securityID = Column(Text)
    securityIDType = Column(Text)
    cusip = Column(Text)
    isin = Column(Text)
    listingExchange = Column(Text)
    underlyingConid = Column(Integer)
    underlyingSymbol = Column(Text)
    underlyingSecurityID = Column(Text)
    underlyingListingExchange = Column(Text)
    issuer = Column(Text)
    multiplier = Column(Float)
    strike = Column(Float)
    expiry = Column(Date)
    tradeID = Column(Text)
    putCall = Column(Text)
    reportDate = Column(Date)
    principalAdjustFactor = Column(Text)
    dateTime = Column(DateTime)
    tradeDate = Column(Date)
    settleDateTarget = Column(Date)
    transactionType = Column(Text)
    exchange = Column(Text)
    quantity = Column(Float)
    tradePrice = Column(Float)
    tradeMoney = Column(Float)
    proceeds = Column(Float)
    taxes = Column(Float)
    ibCommission = Column(Float)
    ibCommissionCurrency = Column(Text)
    netCash = Column(Float)
    closePrice = Column(Float)
    openCloseIndicator = Column(Text)
    notes = Column(Text)
    cost = Column(Float)
    fifoPnlRealized = Column(Float)
    fxPnl = Column(Text)
    mtmPnl = Column(Float)
    origTradePrice = Column(Text)
    origTradeDate = Column(Text)
    origTradeID = Column(Text)
    origOrderID = Column(Text)
    clearingFirmID = Column(Text)
    transactionID = Column(Text)
    buySell = Column(Text)
    ibExecID = Column(Text)
    brokerageOrderID = Column(Text)
    orderReference = Column(Text)
    volatilityOrderLink = Column(Text)
    exchOrderId = Column(Text)
    extExecID = Column(Text)
    orderTime = Column(DateTime)
    openDateTime = Column(Text)
    holdingPeriodDateTime = Column(Text)
    whenRealized = Column(Text)
    whenReopened = Column(Text)
    levelOfDetail = Column(Text)
    changeInPrice = Column(Text)
    changeInQuantity = Column(Text)
    orderType = Column(Text)
    traderID = Column(Text)
    isAPIOrder = Column(Text)
    accruedInt = Column(Float)
    serialNumber = Column(Text)
    deliveryType = Column(Text)
    commodityType = Column(Text)
    fineness = Column(Text)
    weight = Column(Text)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class OrderMapper:
    def cast_to_valid_format(self, record: dict):
        new_record = {}
        for column in _Order.__table__.columns:
            value = record[column.name]
            if value == "":
                new_value = None
            else:
                if column.type.python_type in [str, int, float]:
                    new_value = column.type.python_type(value)
                elif column.type.python_type == date:
                    new_value = datetime.strptime(value, "%Y%m%d").date()
                elif column.type.python_type == datetime:
                    new_value = datetime.strptime(value, "%Y%m%d;%H%M%S")
                else:
                    print(column.type)
                    raise NotImplementedError
            new_record[column.name] = new_value
        return new_record

    def to_dto_list(self, orders: OrderDataFrame) -> List[_Order]:
        records = orders.data_frame.to_dict("records")
        return [_Order(**self.cast_to_valid_format(record)) for record in records]

    def to_dict_list(self, orders: OrderDataFrame):
        dtos = self.to_dto_list(orders)
        return [dto.to_dict() for dto in dtos]


class OrderRepository:
    def __init__(self, rdb_session: RdbSession):
        self.rdb_session = rdb_session
        self.mapper = OrderMapper()

    def create(self, order: _Order):
        with self.rdb_session.write as session:
            session.add(order)

    def update(self, order: _Order):
        with self.rdb_session.write as session:
            session.merge(order)

    def find(self, id):
        with self.rdb_session.read as session:
            return session.query(_Order).filter(_Order.id == id).first()

    def all_limit(self, limit: int = 5000):
        with self.rdb_session.read as session:
            return session.query(_Order).limit(limit).all()

    def delete(self, order: _Order):
        with self.rdb_session.write as session:
            session.query(_Order).filter(_Order.id == order.id).delete()

    def add(self, orders: OrderDataFrame):
        dto_dict_list = self.mapper.to_dict_list(orders)
        with self.rdb_session.write as session:
            session.execute(
                insert(_Order)
                .values(dto_dict_list)
                .on_conflict_do_nothing(
                    constraint=_Order.__table__.primary_key,
                )
            )
