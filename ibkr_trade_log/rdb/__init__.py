from sqlalchemy.orm import declarative_base


class RdbBaseClass(object):
    pass


RdbEntity = declarative_base(cls=RdbBaseClass)
