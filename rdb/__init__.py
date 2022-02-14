from sqlalchemy import Column
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import UUIDType


class RdbBaseClass(object):
    id = Column(UUIDType, primary_key=True, index=True)


RdbEntity = declarative_base(cls=RdbBaseClass)
