from abc import ABC
from dataclasses import asdict
from datetime import datetime
from types import new_class
from typing import TypeVar, Generic, get_args, Optional, List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.elements import BinaryExpression

from bootstrap.logger import LoggerMixin
from bootstrap.rdb.session import RdbSession

DtoType = TypeVar("DtoType")
DomainType = TypeVar("DomainType")


class RdbMapper(Generic[DomainType, DtoType], LoggerMixin, ABC):
    @property
    def domain_type(self):
        return get_args(self.__class__.__orig_bases__[0])[0]  # noqa

    @property
    def dto_type(self):
        return get_args(self.__class__.__orig_bases__[0])[1]  # noqa

    def to_dto(self, domain: DomainType) -> DtoType:
        return self.dto_type(**asdict(domain)) if domain else None

    @staticmethod
    def from_repository(repository):
        name = f"{repository.dto_type.__name__}Mapper"
        return new_class(
            name, (RdbMapper[repository.domain_type, repository.dto_type],), {}
        )()


class RdbRepository(Generic[DomainType, DtoType], LoggerMixin, ABC):
    @property
    def domain_type(self):
        return get_args(self.__class__.__orig_bases__[0])[0]  # noqa

    @property
    def dto_type(self):
        return get_args(self.__class__.__orig_bases__[0])[1]  # noqa

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

    def all_limit(self, order_by: str = None, limit: int = 5000):
        with self.rdb_session.read as session:
            return (
                session.query(self.dto_type)
                .order_by(self.dto_type.dateTime)
                .limit(limit)
                .all()
            )

    def delete(self, dto: DtoType):
        with self.rdb_session.write as session:
            session.query(self.dto_type).filter(self.dto_type.id == dto.id).delete()

    def add_domain_list(self, domain_list: List[DomainType]):
        if len(domain_list) == 0:
            return

        self.logger.debug(
            f"start adding {len(domain_list)} {self.domain_type.__name__}"
        )

        dto_dict_list = [self.mapper.to_dto(domain).to_dict() for domain in domain_list]
        with self.rdb_session.write as session:
            session.execute(
                insert(self.dto_type)
                .values(dto_dict_list)
                .on_conflict_do_nothing(constraint=self.dto_type.__table__.primary_key)
            )

        self.logger.info(
            f"finished adding {len(domain_list)} {self.domain_type.__name__}"
        )

        return

    def filter_by_time(
        self,
        before: Optional[datetime],
        after: Optional[datetime],
    ):
        criteria = self._criteria(before, after)
        with self.rdb_session.write as session:
            return session.query(self.dto_type).filter(*criteria).all()

    def _criteria(
        self,
        before: Optional[datetime],
        after: Optional[datetime],
    ) -> List[BinaryExpression]:
        _criteria = []
        if before is not None:
            _criteria.append(self.dto_type.dateTime <= before)
        if after is not None:
            _criteria.append(self.dto_type.dateTime >= after)
        return _criteria
