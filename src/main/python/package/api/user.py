import json
import os
from glob import glob

import win32api
import win32con

from package.api.constants import USER_DIR, PATH_APP_DATA
from package.api.functions import isname, change_to_uppercase, isint


# load_user() permet de charger le dossier .user et de creer une liste de tout les utilisateur deja enregistrer
def load_users():
    users = []
    load_file = glob(os.path.join(USER_DIR, "*.json"))
    for file in load_file:
        with open(file, "r") as f:
            user_data = json.load(f)
            user_last_name = user_data.get("last_name")
            user_first_name = user_data.get("first_name")
            user_location = user_data.get("location")
            user_monthly_amount = user_data.get("monthly_amount")
            user_manager = user_data.get("manager")
            user = User(user_last_name,
                        user_first_name,
                        user_location,
                        user_monthly_amount,
                        user_manager)
            users.append(user)
    return users


# renvoie une liste de user dont le nom ou prenom sont trouver
def search_user(value):
    found_user = []
    users = load_users()
    for user in users:
        if user.last_name == change_to_uppercase(value):
            found_user.append(user)
        if user.first_name == change_to_uppercase(value):
            found_user.append(user)
    return found_user


class User:
    def __init__(self, last_name, first_name, location=None, monthly_amount=None, manager=False):
        self.last_name = last_name
        self.first_name = first_name
        self.location = location
        self.monthly_amount = monthly_amount
        self.manager = manager

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __repr__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if isname(value):
            self._last_name = change_to_uppercase(value)
        else:
            raise "last name doit etre une chaine de charactere alphabetique"

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if isname(value):
            self._first_name = change_to_uppercase(value)
        else:
            raise "first name doit etre une chaine de charactere alphabetique"

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if value is None:
            self._location = None
        else:
            self._location = change_to_uppercase(value)

    @property
    def monthly_amount(self):
        return self._monthly_amount

    @monthly_amount.setter
    def monthly_amount(self, value):
        if value is None:
            self._monthly_amount = None
        else:
            if isint(value):
                self._monthly_amount = int(value)
            else:
                raise "monthly_amount doit etre un entier"

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, value):
        if isinstance(value, bool):
            self._manager = value
        else:
            raise "manager doit etre un boolean"

    # delete supprime le fichier .json de l'occurence s'il est enregistrer dans .user
    def delete(self):
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return True

    # ismanager verifie si l'occurence (self) est un user manager. Si oui il renvoie True
    @property
    def ismanager(self):
        if self.manager:
            return True
        return False

    @property
    def get_name(self):
        return f"{self.last_name} {self.first_name}"

    def modify(self, last_name=None, first_name=None, location=None, monthly_amount=None, manager=None):
        self.delete()
        self.last_name = last_name
        self.first_name = first_name
        self.location = location
        self.monthly_amount = monthly_amount
        self.manager = manager
        self.save()

    @property
    def path(self):  # cree le chemim vers l'instance actuel dans le dossier tenant
        return os.path.join(USER_DIR, f"{self.last_name}_{self.first_name}_{self.manager}.json")

    # save() permet de sauvegarder l'occurence actuel de la classe user dans le dossier .user
    def save(self):
        users = load_users()
        for user in users:
            if self.last_name == user.last_name:
                if self.first_name == user.first_name:
                    return False
        if not os.path.exists(USER_DIR):
            os.makedirs(USER_DIR)
            win32api.SetFileAttributes(PATH_APP_DATA, win32con.FILE_ATTRIBUTE_HIDDEN)
        data = {"last_name": self.last_name,
                "first_name": self.first_name,
                "location": self.location,
                "monthly_amount": self.monthly_amount,
                "manager": self.manager}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
        return True


if __name__ == '__main__':
    print(load_users())
    print(load_users()[1])
