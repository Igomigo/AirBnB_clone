#!/usr/bin/python3
""" the amenity module"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """ Represents an Amenity
    Attribute:
        name(str) = Name of the Amenity
    """

    name = ""
