from dataclasses import dataclass
from datetime import datetime, date

from sqlalchemy import Column, Text, Float, Integer, Date, DateTime

from bootstrap.ddd import ValueObject
from bootstrap.rdb import RdbEntity
from bootstrap.rdb.repository import RdbRepository


@dataclass(frozen=True)
class Transfer(ValueObject):
    transactionID: str
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
    quantity: float
    fxPnl: str
    acctAlias: str
    model: str
    securityID: str
    securityIDType: str
    cusip: str
    isin: str
    underlyingSecurityID: str
    underlyingListingExchange: str
    issuer: str
    principalAdjustFactor: str
    serialNumber: str
    deliveryType: str
    commodityType: str
    fineness: str
    weight: str
    date: date
    type: str
    direction: str
    company: str
    account: str
    accountName: str
    deliveringBroker: str
    transferPrice: float
    positionAmount: float
    positionAmountInBase: float
    pnlAmount: float
    pnlAmountInBase: float
    cashTransfer: float
    code: str
    clientReference: str


class _Transfer(RdbEntity):
    __tablename__ = "ibkr_transfers"
    transactionID = Column(Text, primary_key=True)

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
    quantity = Column(Float)
    fxPnl = Column(Text)
    acctAlias = Column(Text)
    model = Column(Text)
    securityID = Column(Text)
    securityIDType = Column(Text)
    cusip = Column(Text)
    isin = Column(Text)
    underlyingSecurityID = Column(Text)
    underlyingListingExchange = Column(Text)
    issuer = Column(Text)
    principalAdjustFactor = Column(Text)
    serialNumber = Column(Text)
    deliveryType = Column(Text)
    commodityType = Column(Text)
    fineness = Column(Text)
    weight = Column(Text)
    date = Column(Date)
    type = Column(Text)
    direction = Column(Text)
    company = Column(Text)
    account = Column(Text)
    accountName = Column(Text)
    deliveringBroker = Column(Text)
    transferPrice = Column(Float)
    positionAmount = Column(Float)
    positionAmountInBase = Column(Float)
    pnlAmount = Column(Float)
    pnlAmountInBase = Column(Float)
    cashTransfer = Column(Float)
    code = Column(Text)
    clientReference = Column(Text)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class TransferRepository(RdbRepository[Transfer, _Transfer]):
    pass
