#!/usr/bin/python3
"""this module contains a program that contains the entry point
    of the command interpreter
 Console Module """

import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.__init__ import storage


class HBNBCommand(cmd.Cmd):
    '''the class that implements a command intepreter'''

    classes = {"BaseModel": BaseModel, "User": User,
               "Place": Place, "State": State, "City": City,
               "Amenity": Amenity, "Review": Review}
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }
    prompt = "(hbnb) "

    def default(self, line):
        '''Handle commands with specified syntax'''
        if "." in line:
            args = line.split(".")
            cls_name = args[0]
            cmd = args[1]
            if cmd == "count()":
                self.do_count(cls_name)
            elif cmd == "all()":
                self.do_all(cls_name)
            elif cmd.startswith("show("):
                cls_id = cmd.split('"')[1]
                self.do_show(cls_name + " " + cls_id)
            elif cmd.startswith("destroy("):
                cls_id = cmd.split('"')[1]
                self.do_destroy(cls_name + " " + cls_id)
            elif cmd.startswith("update("):
                if "{" in cmd:
                    cmd_args = cmd.split('(')[1].split(')')[0].split(
                        ',', maxsplit=1)
                    cls_id = cmd_args[0].strip().strip('"')
                    dict1 = eval(cmd_args[1])
                    for k, v in dict1.items():
                        self.do_update(cls_name+" "+cls_id+" "+k+" "+str(v))
                else:
                    cls_id = cmd.split('"')[1]
                    name = cmd.split('"')[3]
                    val = cmd.split('"')[5]
                    self.do_update(cls_name+" "+cls_id+" "+name+" "+val)

    def do_quit(self, line):
        '''To exit my wonderful command intepreter'''
        return True

    def help_quit(self):
        '''help info on quitting the program'''
        print("quit the program with <quit>\n")

    def do_EOF(self, line):
        "also to exit my program\n"
        print()
        return True

    def help_EOF(self):
        '''help info on EOF'''
        print("Exit the program with <Ctrl + d>\n")

    def emptyline(self):
        "nothing happens with an emptyline.\n"
        pass

    def do_create(self, arg):
        '''Creates a new instance of any class'''
        if arg == "":
            print("** class name missing **")
        elif arg not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            new_instance = HBNBCommand.classes[arg]()
            new_instance.save()
            print(new_instance.id)
            new_instance.save()

    def help_create(self):
        '''help info on the create command'''
        print("creates a new existing class")
        print("USAGE: create <class name>\n")

    def do_show(self, arg):
        '''Shows an individual object'''
        if len(arg) == 0:
            print("** class name missing **")
            return

        if len(arg) >= 1:
            new = arg.split()
            cls_name = new[0]
            if len(new) > 1:
                cls_id = new[1]
            else:
                cls_id = None

            if cls_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            if not cls_id:
                print("** instance id missing **")
                return

        key = cls_name + "." + cls_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        '''help info on the show command'''
        print("shows an existing class")
        print("USAGE: show <class name> <objects id>\n")

    def do_count(self, line):
        '''retrieves the number of a class present in the storage\n'''
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if k.split(".")[0] == line:
                count += 1
        print(count)

    def help_count(self):
        '''help info on the count command'''
        print("counts a specific class")
        print("USAGE: count <class name>\n")

    def do_destroy(self, args):
        '''Destroys a specified object\n'''
        if len(args) == 0:
            print("** class name missing **")
            return

        if len(args) >= 1:
            new = args.split()
            c_name = new[0]
            if len(new) > 1:
                c_id = new[1]
            else:
                c_id = None

            if c_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            if not c_id:
                print("** instance id missing **")
                return

            key = c_name + "." + c_id

            try:
                del (storage.all()[key])
                storage.save()
            except KeyError:
                print("** no instance found **")

    def help_destroy(self):
        '''help info on the destroy command'''
        print("deletes a specific class")
        print("USAGE: destroy <class name> <objects id>\n")

    def do_all(self, args):
        """Shows all objects, or all objects of a class\n"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                cls_name = k.split(".")
                if cls_name[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        '''help info on the all command'''
        print("show a class or all existing class")
        print("USAGE: all <class name>\n")

    def do_update(self, args):
        """Updates a certain object with new info\n """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        '''help info on the update command'''
        print("updates a specific class")
        print("USAGE: update <class name> <objects id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
