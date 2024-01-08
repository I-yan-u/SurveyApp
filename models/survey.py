from models.base import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship

class Survey(BaseModel, Base):
    __tablename__ = 'survey'
    creators_id = Column('creators_id', String(60), ForeignKey('users.id'), nullable=False)
    title = Column('title', String(60), nullable=False)
    description = Column('description', String(256), nullable=False)
    form = Column('form', Text, nullable=False)
    # response = relationship('Response', back_populates='survey', cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        """Create the instance"""
        super().__init__(**kwargs)
