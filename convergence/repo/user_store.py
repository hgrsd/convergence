from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from convergence import exceptions
from convergence.repo import Store
from convergence.models import User


class UserStore(Store):

    def __init__(self, session=None):
        super().__init__(session)

    def get_user_by_email(self, email):
        """
        Return user for provided email address
        :param email: email address
        :return: User object
        """
        return self.session.query(User).filter_by(email=email).first()

    def get_user_by_id(self, user_id):
        """
        Return user for provided user id
        :param user_id: user id
        :return: User object
        """
        return self.session.query(User).get(user_id)

    def get_users_by_ids(self, user_ids):
        """
        Return users for provided user ids
        :param user_ids: list of user ids
        :return: list of User objects
        """
        return self.session.query(User).filter(User.id.in_(user_ids)).all()

    def add_user(self, user):
        """
        Add user to database
        :param user: User object
        """
        self.session.add(user)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            if isinstance(e, IntegrityError):
                raise exceptions.InputError("Email address in use.")
            else:
                raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None

    def delete_user(self, user):
        """
        Delete user from database
        :param user: User object
        """
        self.session.delete(user)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise exceptions.DatabaseError(f"Error: {str(e)}")
        return None

    def commit_changes(self):
        """Commit changes in session object to database"""
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            raise exceptions.DatabaseError(f"Error: {str(e)}")
