import models
from bcrypt import hashpw, gensalt
from models.base import Base, BaseModel
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    __tablename__ = 'users'
    first_name = Column('first_name', String(60), nullable=False)
    last_name = Column('last_name', String(60), nullable=False)
    email = Column('email', String(60), nullable=False, unique=True)
    password = Column('password', String(60), nullable=False)
    creator = Column('creator', Boolean, default=False)
    session_id = Column('session_id', String(250), nullable=True)
    reser_token = Column('reser_token', String(250), nullable=True)

    def __init__(self, **kwargs):
        """Create the instance"""
        super().__init__(**kwargs)

