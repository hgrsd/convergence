import sqlalchemy

from . import models


class ConvergenceDB:
    """Set up a db object using the models from models.py"""
    def __init__(self, db_url):
        """Set up engine and session"""
        self.engine = sqlalchemy.create_engine(db_url)
        self.base = models.base
        self.metadata = models.base.metadata
        self._SessionMaker = sqlalchemy.orm.sessionmaker(bind=self.engine)

    def initialise_tables(self):
        """Initialise all tables defined in models.py"""
        session = self.create_session()
        self.base.metadata.create_all(self.engine)
        session.commit()

    def create_session(self):
        return self._SessionMaker()
