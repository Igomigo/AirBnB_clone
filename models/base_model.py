"""
This module contains the BaseModel class that defines
all common attributes for other classes
"""
from uuid import uuid4
from datetime import datetime
import models

time_for = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """ The BaseModel class"""

    def __init__(self, *args, **kwargs):
        """ the class constructor that initializes a new BaseModel
        Args:
            *args: not used
            **kwargs: represents the key/value pairs of attributes
        """

        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)
            self.created_at = datetime.strptime(kwargs["created_at"], time_for)
            self.updated_at = datetime.strptime(kwargs["updated_at"], time_for)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """ returns a string representation of an instance """
        return "[{}] ({}) {}".format(
                               self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """ updates the public instance attribute "updated_at"
        with the current datetime """

        self.updated_at = datetime.now()

    def to_dict(self):
        """ returns a dictionary containing all
        keys/values of __dict__ of the instance """

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict
