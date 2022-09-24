from dataclasses import dataclass
from datetime import datetime, date

from sqlalchemy import Column, Text, Float, Integer, Date, DateTime

from bootstrap.ddd import ValueObject
from bootstrap.rdb import RdbEntity
from bootstrap.rdb.repository import RdbRepository


@dataclass(frozen=True)
class CashTransaction(ValueObject):
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
    levelOfDetail: str
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
    serialNumber: str
    deliveryType: str
    commodityType: str
    fineness: str
    weight: str
    settleDate: date
    amount: float
    type: str
    code: str
    clientReference: str

    @classmethod
    def from_flex(cls, flex):
        flex_dict = flex.__dict__
        domain_dict = {}
        for key, value in flex_dict.items():
            if value == "":
                new_value = None
            else:
                key_type = cls.__annotations__[key]
                if key_type in [str, int, float]:
                    new_value = key_type(value)
                elif key_type == date:
                    new_value = datetime.strptime(value, "%Y%m%d").date()
                elif key_type == datetime:
                    if ";" in value:
                        new_value = datetime.strptime(value, "%Y%m%d;%H%M%S")
                    else:
                        # Some datetime field has not time attribute in the ibkr flex report
                        new_value = datetime.strptime(value, "%Y%m%d")
                else:
                    raise NotImplementedError
            domain_dict[key] = new_value
        return cls(**domain_dict)


class _CashTransaction(RdbEntity):
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


class CashTransactionRepository(RdbRepository[CashTransaction, _CashTransaction]):
    pass
