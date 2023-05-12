#!/usr/bin/python3
"""
Module that contains the City class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    Represents a city.
    Attributes:
         state_id(str) = The state id
         name(str) = The city name
    """

    state_id = ""
    name = ""
