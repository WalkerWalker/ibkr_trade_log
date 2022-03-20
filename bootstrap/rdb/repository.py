from abc import ABCMeta
from datetime import date, datetime
from types import new_class
from typing import List, TypeVar, Generic, get_args

from sqlalchemy.dialects.postgresql import insert

from bootstrap.rdb.session import RdbSession

DataFrameType = TypeVar("DataFrameType")
RecordType = TypeVar("RecordType")


class RdbMapper(Generic[DataFrameType, RecordType], metaclass=ABCMeta):
    @property
    def data_frame_type(self):
        return get_args(self.__class__.__orig_bases__[0])[0]  # noqa

    @property
    def record_type(self):
        return get_args(self.__class__.__orig_bases__[0])[1]  # noqa

    def cast_to_valid_format(self, record: dict):
        new_record = {}
        for column in self.record_type.__table__.columns:
            value = record[column.name]
            if value == "":
                new_value = None
            else:
                if column.type.python_type in [str, int, float]:
                    new_value = column.type.python_type(value)
                elif column.type.python_type == date:
                    new_value = datetime.strptime(value, "%Y%m%d").date()
                elif column.type.python_type == datetime:
                    if ";" in value:
                        new_value = datetime.strptime(value, "%Y%m%d;%H%M%S")
                    else:
                        # Some datetime field has not time attribute in the ibkr report
                        new_value = datetime.strptime(value, "%Y%m%d")
                else:
                    print(column.type)
                    raise NotImplementedError
            new_record[column.name] = new_value
        return new_record

    def to_record_list(self, record_df: DataFrameType) -> List[RecordType]:
        records = record_df.data_frame.to_dict("records")
        return [
            self.record_type(**self.cast_to_valid_format(record)) for record in records
        ]

    def to_dict_list(self, record_df: DataFrameType):
        record_list = self.to_record_list(record_df)
        return [record.to_dict() for record in record_list]

    @staticmethod
    def from_repository(repository):
        name = f"{repository.data_frame_type.__module__}.{repository.record_type.__name__}Mapper"
        return new_class(
            name, (RdbMapper[repository.data_frame_type, repository.record_type],), {}
        )()


class RdbRepository(Generic[DataFrameType, RecordType], metaclass=ABCMeta):
    @property
    def data_frame_type(self):
        return get_args(self.__class__.__orig_bases__[0])[0]  # noqa

    @property
    def record_type(self):
        return get_args(self.__class__.__orig_bases__[0])[1]  # noqa

    def __init__(self, rdb_session: RdbSession):
        self.rdb_session = rdb_session
        self.mapper = RdbMapper.from_repository(self)

    def create(self, order: RecordType):
        with self.rdb_session.write as session:
            session.add(order)

    def update(self, order: RecordType):
        with self.rdb_session.write as session:
            session.merge(order)

    def find(self, id):
        with self.rdb_session.read as session:
            return (
                session.query(self.record_type)
                .filter(self.record_type.id == id)
                .first()
            )

    def all_limit(self, limit: int = 5000):
        with self.rdb_session.read as session:
            return session.query(self.record_type).limit(limit).all()

    def delete(self, order: RecordType):
        with self.rdb_session.write as session:
            session.query(self.record_type).filter(
                self.record_type.id == order.id
            ).delete()

    def add(self, record_set: DataFrameType):
        if record_set.data_frame is None:
            return
        record_dict_list = self.mapper.to_dict_list(record_set)
        with self.rdb_session.write as session:
            session.execute(
                insert(self.record_type)
                .values(record_dict_list)
                .on_conflict_do_nothing(
                    constraint=self.record_type.__table__.primary_key,
                )
            )