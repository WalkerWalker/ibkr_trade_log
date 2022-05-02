from abc import ABC
from datetime import date, datetime
from types import new_class
from typing import TypeVar, Generic, get_args

from sqlalchemy.dialects.postgresql import insert

from bootstrap.logger import LoggerMixin
from bootstrap.rdb.session import RdbSession

DtoType = TypeVar("DtoType")


class RdbMapper(Generic[DtoType], LoggerMixin, ABC):
    @property
    def dto_type(self):
        return get_args(self.__class__.__orig_bases__[0])[0]  # noqa

    def domain_to_dto_dict(self, domain):
        dto_dict = {}
        for column in self.dto_type.__table__.columns:
            value = getattr(domain, column.name)
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
                    self.logger.error(f"unexpected type{column.type}")
                    raise NotImplementedError
            dto_dict[column.name] = new_value
        return dto_dict

    def domain_to_dto(self, domain):
        dto_dict = self.domain_to_dto_dict(domain)
        return self.dto_type(**dto_dict)

    @staticmethod
    def from_repository(repository):
        name = f"{repository.dto_type.__name__}Mapper"
        return new_class(name, (RdbMapper[repository.dto_type],), {})()


class RdbRepository(Generic[DtoType], LoggerMixin, ABC):
    @property
    def dto_type(self):
        return get_args(self.__class__.__orig_bases__[0])[0]  # noqa

    def __init__(self, rdb_session: RdbSession):
        self.rdb_session = rdb_session
        self.mapper = RdbMapper.from_repository(self)

    def create(self, dto: DtoType):
        with self.rdb_session.write as session:
            session.add(dto)

    def update(self, dto: DtoType):
        with self.rdb_session.write as session:
            session.merge(dto)

    def find(self, id):
        with self.rdb_session.read as session:
            return session.query(self.dto_type).filter(self.dto_type.id == id).first()

    def all_limit(self, limit: int = 5000):
        with self.rdb_session.read as session:
            return session.query(self.dto_type).limit(limit).all()

    def delete(self, dto: DtoType):
        with self.rdb_session.write as session:
            session.query(self.dto_type).filter(self.dto_type.id == dto.id).delete()

    def add_domain_list(self, domain_list: list):
        if len(domain_list) == 0:
            return

        self.logger.info(f"start adding {len(domain_list)} {self.dto_type.__name__}")

        dto_dict_list = [
            self.mapper.domain_to_dto_dict(domain) for domain in domain_list
        ]
        with self.rdb_session.write as session:
            return session.execute(
                insert(self.dto_type)
                .values(dto_dict_list)
                .on_conflict_do_nothing(constraint=self.dto_type.__table__.primary_key)
            )
