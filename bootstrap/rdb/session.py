from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from bootstrap.rdb import RdbEntity
from bootstrap.rdb.config import RdbConfig


class RdbSession:
    def __init__(self, engine, session_maker, session: Session):
        self.engine = engine
        self.session_maker = session_maker
        self.session = session
        self._lock = Lock()
        self._transaction = None

    def __enter__(self):
        self._lock.__enter__()
        self._transaction = self.session.begin()
        self._transaction.__enter__()

        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._transaction.__exit__(exc_type, exc_val, exc_tb)
        self._transaction = None
        self._lock.__exit__(exc_type, exc_val, exc_tb)

    @property
    def write(self):
        return self

    @property
    def read(self):
        return RdbSession(
            engine=self.engine,
            session_maker=self.session_maker,
            session=self.session_maker(),
        )


class RdbSessionFactory:
    def __init__(self, config: RdbConfig, metadata=RdbEntity.metadata):
        self.config = config
        self.engine = create_engine(
            self.config.build_url(),
        )

        self.metadata = metadata

        self.session_maker = sessionmaker(
            autocommit=self.config.autocommit,
            autoflush=self.config.autoflush,
            bind=self.engine,
        )

    def startup(self):
        self.metadata.create_all(bind=self.engine)

    def build(self) -> RdbSession:
        return RdbSession(
            engine=self.engine,
            session_maker=self.session_maker,
            session=self.session_maker(),
        )
