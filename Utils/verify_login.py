from flask import request, redirect
from pyotp import totp
from werkzeug.exceptions import BadRequestKeyError


def verify_login(database):
    token = request.cookies.get('token')
    try:
        if database.select("""SELECT desactivated FROM cantina_administration.user WHERE token = %s""", (token,), 1)[0]:
            return "desactivated"
    except TypeError:
        return False

    token_validation = database.select("""SELECT id FROM cantina_administration.user WHERE token=%s""", (token,),
                                       number_of_data=1)
    validation = request.cookies.get('validation')
    validation_from_db = database.select("""SELECT content FROM cantina_administration.config WHERE name=%s""",
                                         ("secret_token",), number_of_data=1)

    return True if token_validation is not None and validation == validation_from_db[0] else False


def verify_A2F(database):
    try:
        key = totp.TOTP(database.select('''SELECT A2F_secret FROM cantina_administration.user WHERE username=%s''',
                                        (request.form['username']), number_of_data=1)[0])
    except BadRequestKeyError:
        key = totp.TOTP(database.select('''SELECT A2F_secret FROM cantina_administration.user WHERE token=%s''',
                                        (request.cookies.get('token')), number_of_data=1)[0])
    return key.verify(request.form['2fa-code'].replace(" ", ""))
