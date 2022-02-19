from dataclasses import dataclass
from typing import List

from pandas import DataFrame
from sqlalchemy import Column, Text
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
    fxRateToBase = Column(Text)
    assetCategory = Column(Text)
    symbol = Column(Text)
    description = Column(Text)
    conid = Column(Text)
    securityID = Column(Text)
    securityIDType = Column(Text)
    cusip = Column(Text)
    isin = Column(Text)
    listingExchange = Column(Text)
    underlyingConid = Column(Text)
    underlyingSymbol = Column(Text)
    underlyingSecurityID = Column(Text)
    underlyingListingExchange = Column(Text)
    issuer = Column(Text)
    multiplier = Column(Text)
    strike = Column(Text)
    expiry = Column(Text)
    tradeID = Column(Text)
    putCall = Column(Text)
    reportDate = Column(Text)
    principalAdjustFactor = Column(Text)
    dateTime = Column(Text)
    tradeDate = Column(Text)
    settleDateTarget = Column(Text)
    transactionType = Column(Text)
    exchange = Column(Text)
    quantity = Column(Text)
    tradePrice = Column(Text)
    tradeMoney = Column(Text)
    proceeds = Column(Text)
    taxes = Column(Text)
    ibCommission = Column(Text)
    ibCommissionCurrency = Column(Text)
    netCash = Column(Text)
    closePrice = Column(Text)
    openCloseIndicator = Column(Text)
    notes = Column(Text)
    cost = Column(Text)
    fifoPnlRealized = Column(Text)
    fxPnl = Column(Text)
    mtmPnl = Column(Text)
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
    orderTime = Column(Text)
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
    accruedInt = Column(Text)
    serialNumber = Column(Text)
    deliveryType = Column(Text)
    commodityType = Column(Text)
    fineness = Column(Text)
    weight = Column(Text)


class OrderMapper:
    def to_dto_list(self, orders: OrderDataFrame) -> List[_Order]:
        records = orders.data_frame.to_dict("records")
        return [_Order(**record) for record in records]

    def to_dict_list(self, orders: OrderDataFrame):
        return orders.data_frame.to_dict("records")


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
