# verifie si l'argument est un nom correct, sans chiffre ni symbole
import os
import subprocess


def isname(value):
    try:
        value_ = "".join(value.split())  # .split() decoupe un str en liste et "".join rassemble une liste en un str
    except AttributeError:
        return False
    if value_.isalpha():  # isalpha() renvoie false si le str contient des int ou des caratere != de l'alphabet
        return True
    return False


# change le str en majuscule et supprime les espace au debut et a la fin
def change_to_uppercase(value):
    value_upper = value.upper()
    return " ".join(value_upper.split())


# renvoie true si une variable est int
def isint(value):
    if isinstance(value, int):  # isinstance() verifie si la valeur donner est du bon type
        return True
    return False


##############################WARNING##################################
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')


def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
