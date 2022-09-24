from dataclasses import dataclass
from datetime import datetime, date

from sqlalchemy import Column, Text, Float, Integer, Date, DateTime

from bootstrap.ddd import ValueObject
from bootstrap.rdb import RdbEntity
from bootstrap.rdb.repository import RdbRepository


@dataclass(frozen=True)
class Order(ValueObject):
    ibOrderID: str
    accountId: str
    currency: str
    fxRateToBase: float
    assetCategory: str
    symbol: str
    description: str
    conid: int
    listingExchange: str
    underlyingConid: int
    underlyingSymbol: str
    multiplier: float
    strike: float
    expiry: date
    putCall: str
    reportDate: date
    dateTime: datetime
    tradeDate: date
    settleDateTarget: date
    quantity: float
    tradePrice: float
    tradeMoney: float
    proceeds: float
    taxes: float
    ibCommission: float
    ibCommissionCurrency: str
    netCash: float
    closePrice: float
    openCloseIndicator: str
    notes: str
    cost: float
    fifoPnlRealized: float
    fxPnl: str
    mtmPnl: float
    buySell: str
    orderTime: datetime
    levelOfDetail: str
    orderType: str
    isAPIOrder: str
    # TODO useless columns in the following
    acctAlias: str
    model: str
    securityID: str
    securityIDType: str
    cusip: str
    isin: str
    underlyingSecurityID: str
    underlyingListingExchange: str
    issuer: str
    tradeID: str
    principalAdjustFactor: str
    transactionType: str
    exchange: str
    origTradePrice: str
    origTradeDate: str
    origTradeID: str
    origOrderID: str
    clearingFirmID: str
    transactionID: str
    ibExecID: str
    brokerageOrderID: str
    orderReference: str
    volatilityOrderLink: str
    exchOrderId: str
    extExecID: str
    openDateTime: str
    holdingPeriodDateTime: str
    whenRealized: str
    whenReopened: str
    changeInPrice: str
    changeInQuantity: str
    traderID: str
    accruedInt: float
    serialNumber: str
    deliveryType: str
    commodityType: str
    fineness: str
    weight: str

    @classmethod
    def from_flex_order(cls, flex_order):
        return cls(**flex_order.__dict__)


class _Order(RdbEntity):
    __tablename__ = "ibkr_orders"
    ibOrderID = Column(Text, primary_key=True)
    accountId = Column(Text)
    currency = Column(Text)
    fxRateToBase = Column(Float)
    assetCategory = Column(Text)
    symbol = Column(Text)
    description = Column(Text)
    conid = Column(Integer)
    listingExchange = Column(Text)
    underlyingConid = Column(Integer)
    underlyingSymbol = Column(Text)
    multiplier = Column(Float)
    strike = Column(Float)
    expiry = Column(Date)
    putCall = Column(Text)
    reportDate = Column(Date)
    dateTime = Column(DateTime)
    tradeDate = Column(Date)
    settleDateTarget = Column(Date)
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
    buySell = Column(Text)
    orderTime = Column(DateTime)
    levelOfDetail = Column(Text)
    orderType = Column(Text)
    isAPIOrder = Column(Text)
    # TODO useless columns in the following
    acctAlias = Column(Text)
    model = Column(Text)
    securityID = Column(Text)
    securityIDType = Column(Text)
    cusip = Column(Text)
    isin = Column(Text)
    underlyingSecurityID = Column(Text)
    underlyingListingExchange = Column(Text)
    issuer = Column(Text)
    tradeID = Column(Text)
    principalAdjustFactor = Column(Text)
    transactionType = Column(Text)
    exchange = Column(Text)
    origTradePrice = Column(Text)
    origTradeDate = Column(Text)
    origTradeID = Column(Text)
    origOrderID = Column(Text)
    clearingFirmID = Column(Text)
    transactionID = Column(Text)
    ibExecID = Column(Text)
    brokerageOrderID = Column(Text)
    orderReference = Column(Text)
    volatilityOrderLink = Column(Text)
    exchOrderId = Column(Text)
    extExecID = Column(Text)
    openDateTime = Column(Text)
    holdingPeriodDateTime = Column(Text)
    whenRealized = Column(Text)
    whenReopened = Column(Text)
    changeInPrice = Column(Text)
    changeInQuantity = Column(Text)
    traderID = Column(Text)
    accruedInt = Column(Float)
    serialNumber = Column(Text)
    deliveryType = Column(Text)
    commodityType = Column(Text)
    fineness = Column(Text)
    weight = Column(Text)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class OrderRepository(RdbRepository[_Order]):
    pass
