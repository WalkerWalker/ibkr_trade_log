from dataclasses import dataclass

from pandas import DataFrame
from sqlalchemy import Column, Text, Float, Integer, Date, DateTime

from bootstrap.ddd import ValueObject
from bootstrap.rdb import RdbEntity
from bootstrap.rdb.repository import RdbRepository


@dataclass(frozen=True)
class CashTransactionDataFrame(ValueObject):
    data_frame: DataFrame


class CashTransaction(RdbEntity):
    __tablename__ = "ibkr_cash_transactions"

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
    levelOfDetail = Column(Text)
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
    serialNumber = Column(Text)
    deliveryType = Column(Text)
    commodityType = Column(Text)
    fineness = Column(Text)
    weight = Column(Text)
    settleDate = Column(Date)
    amount = Column(Float)
    type = Column(Text)
    code = Column(Text)
    clientReference = Column(Text)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class CashTransactionRepository(RdbRepository[CashTransaction]):
    pass
