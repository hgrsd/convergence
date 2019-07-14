"""
Store base class
"""
from convergence import db


class Store:

    def __init__(self, session):
        """
        Initialise class instance using session (if provided),
        otherwise create new session.
        :param session: session object or None
        """
        self.session = session if session else db.create_session()
