"""
Base class for database objects
"""

from typing import Any
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models
from models.idmaker import getRID, getSID, getUID
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()

class BaseModel:
    """ Base class for database models"""
    id = Column("id", String(60), primary_key=True)
    created_at = Column("created_at", DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                if self.__class__.__name__ == 'User':
                    self.id = getUID()
                elif self.__class__.__name__ == 'Survey':
                    self.id = getSID()
                else:
                    self.id = getRID()
        else:
            if self.__class__.__name__ == 'User':
                self.id = getUID()
            elif self.__class__.__name__ == 'Survey':
                self.id = getSID()
            else:
                self.id = getRID()

    def __str__(self):
        """ returns a string representation of the object"""
        return "({}) - [{}]".format(self.__class__.__name__, self.id)
    
    def __repr__(self):
        """Complex representation of the object """
        return "({}) - [{}]".format(self.__class__.__name__, self.to_dict())
    
    def save(self):
        """ saves the object"""
        models.store.new(self)
        models.store.save()

    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if "password" in new_dict:
            del new_dict["password"]
        return new_dict
    
    def delete(self):
        """delete the current instance from the storage"""
        models.store.delete(self)
