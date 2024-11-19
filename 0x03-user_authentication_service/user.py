from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User class represents a user in the database.

    Attributes:
        id (int): Unique identifier for the user.
        email (str): Email address of the user.
        hashed_password (str): Hashed password of the user.
        session_id (str, optional): Session ID for the user's current session.
        reset_token (str, optional): Token used to reset user's password.

    Methods:
        __repr__: Returns a string representation of the User instance.
    """
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        return "<User(id='%s', email='%s')>" % (
                                self.id, self.email)
