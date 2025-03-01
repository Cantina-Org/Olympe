from flask import request, jsonify
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from werkzeug.exceptions import BadRequestKeyError
from pyotp import totp


def api_login_cogs(database, error):
    status_code = 200
    credentials_status = False
    unique_id = ""
    secret_id = ""
    username = request.json['username']  # Sauvegarde du nom d'utilisateur
    password = request.json['password']  # Sauvegarde du mot de passe

    # Séléction des données requise pour valider la connexion.
    row = database.select("""SELECT password, token, A2F FROM cantina_administration.user WHERE username = %s""",
                          (username,), number_of_data=1)

    validation_code = database.select("""SELECT content FROM cantina_pensive.config WHERE name=%s""",
                                      ('secret_token',), number_of_data=1)

    try:
        dfa_code = request.json['dfa_code']  # Sauvegarde du code d'A2F si l'utilisateur en à rempli un
    except BadRequestKeyError:
        dfa_code = None

    if row is None:  # Si aucune correspondance, redirect vers la page de login avec le message d'erreur n°1
        status_code = 401

    try:
        PasswordHasher().verify(row[0], password)  # Verification de la correspondance du MDP

        if row[2] and dfa_code is None or row[2] and not dfa_code:
            # Si l'A2F est activé, mais qu'aucun code n'est fournis
            status_code = 418
        elif not row[2] or verify_A2F(database):  # Si l'A2F n'est pas activé ou que le code est correcte
            credentials_status = True
            unique_id = row[1]
            secret_id = validation_code[0]
        else:  # Dans tout les autres cas
            status_code = 401

    except VerifyMismatchError:  # Si le MDP ne correspond pas, redirect vers le login avec le message d'erreur n°1
        status_code = 401
    except TypeError:
        status_code = 401

    json_to_send = {
        "status_code": status_code,
        "credentials_status": credentials_status,
        "unique_id": unique_id,
        "secret_id": secret_id
    }
    print(jsonify(json_to_send))
    return jsonify(json_to_send)


def verify_A2F(database):
    try:
        key = totp.TOTP(database.select('''SELECT A2F_secret FROM cantina_administration.user WHERE username=%s''',
                                        (request.json['username']), number_of_data=1)[0])
        return key.verify(request.json['dfa_code'].replace(" ", ""))

    except BadRequestKeyError:
        return None
