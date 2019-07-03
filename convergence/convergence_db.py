import sqlalchemy

from . import models


class ConvergenceDB:
    """Set up a db object using the models from models.py"""
    def __init__(self, db_url):
        """Set up engine and session"""
        self.engine = sqlalchemy.create_engine(db_url)
        self.base = models.base
        self.metadata = models.base.metadata
        SessionMaker = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = SessionMaker()

    def create_tables(self):
        """Create tables used in models.py"""
        self.base.metadata.create_all(self.engine)
        self.session.commit()
