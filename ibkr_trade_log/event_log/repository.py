from sqlalchemy import Column, Text

from bootstrap.rdb import RdbEntity
from bootstrap.rdb.repository import RdbRepository


class IbkrEvent(RdbEntity):
    __tablename__ = "ibkr_event_log"
    time = Column(Text, primary_key=True)
    event_id = Column(Text, primary_key=True)
    event_type = Column(Text, primary_key=True)


class EventRepository(RdbRepository[IbkrEvent]):
    pass
