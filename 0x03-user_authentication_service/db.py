#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db",
                                     echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        Args:
            email (str): The user's email
            hashed_password (str): The user's hashed password
        Returns:
            User: The newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments
        Args:
            kwargs: Arbitrary keyword arguments to filter the users table
        Returns:
            User: The first User object that matches the filter criteria
        Raises:
            NoResultFound: If no user is found
            InvalidRequestError: If the query is invalid
        """
        try:
            all_users = self._session.query(User)
            for k, v in kwargs.items():
                if k not in User.__dict__:
                    raise InvalidRequestError
                for usr in all_users:
                    if usr.__dict__[k] == v:
                        return usr
            raise NoResultFound
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes
        Args:
            user_id (int): The user's ID
            kwargs: Arbitrary keyword arguments to update the user's attributes
        Returns:
            None
        Raises:
            ValueError: If an argument does not correspond to a user attribute
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        self._session.commit()
