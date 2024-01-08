from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class Response(BaseModel, Base):
    __tablename__ = 'response'
    users_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    survey_id = Column(String(60), ForeignKey('survey.id'), nullable=False)
    title = Column('title', String(24), nullable=False)
    response = Column('response', Text, nullable=False)

    def __init__(self, **kwargs):
        """Create the instance"""
        super().__init__(**kwargs)
