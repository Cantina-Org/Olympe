from werkzeug.exceptions import BadRequestKeyError
from flask import request


def check_perm(perm_name):
    try:
        return 1 if request.form[perm_name] else 0  # Vérifie si perm_name existe dans le formulaire.
    except BadRequestKeyError:
        return 0
