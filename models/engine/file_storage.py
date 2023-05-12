#!/usr/bin/python3
""" module that contains the FileStorage class """
from models.base_model import BaseModel
import json
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """ file storage class that serializes instances to a JSON file
    and deserializes JSON file to instances """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the __objects dictionary """

        return self.__objects

    def new(self, obj):
        """Stores all instances created from any class
        that inherits from the BaseModel in the '__object' variable
        as values with the key <obj class name>.id.
        This is done in order to easily located any instance
        by just the instance's class name and id.
        """

        obj_key = "{}.{}".format(self.__class__.__name__, obj.id)
        self.__objects[obj_key] = obj

    def save(self):
        """Serializes __objects to the JSON file '__file_path'"""

        js = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as jsonfile:
            json.dump(js, jsonfile)

    def reload(self):
        """Deserializes JSON file into __objects."""

        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for key, obj in data.items():
                    newObj = eval(obj['__class__'])(**obj)
                    self.__objects[key] = newObj
        except FileNotFoundError:
            pass
