from flask import request
from pyotp import totp


def verify_login(database):
    token = request.cookies.get('token')
    token_validation = database.select("""SELECT id FROM cantina_administration.user WHERE token=%s""", (token,),
                                       number_of_data=1)
    validation = request.cookies.get('validation')
    validation_from_db = database.select("""SELECT content FROM cantina_administration.config WHERE name=%s""",
                                         ("secret_token",), number_of_data=1)

    return True if token_validation is not None and validation == validation_from_db[0] else False


def verify_A2F(database):
    key = totp.TOTP(database.select('''SELECT A2F_secret FROM cantina_administration.user WHERE token=%s''',
                                    (request.cookies.get('token')), number_of_data=1)[0])
    return key.verify(request.form['a2f-code'].replace(" ", ""))
