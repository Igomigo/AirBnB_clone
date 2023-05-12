#!/usr/bin/python3
"""
module that contains the user class
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    The User class that inherits from BaseModel.

    attributes:
         email(str): user's email
         password(str): user's password
         first_name(str): user's firstname
         last_name(str): user's lastname
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
