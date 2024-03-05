from flask import request


def verify_login(database):
    token = request.cookies.get('token')
    token_validation = database.select("""SELECT id FROM cantina_administration.user WHERE token=%s""", (token,),
                                       number_of_data=1)
    validation = request.cookies.get('validation')
    validation_from_db = database.select("""SELECT content FROM cantina_administration.config WHERE name=%s""",
                                         ("secret_token",), number_of_data=1)

    return True if token_validation is not None and validation == validation_from_db[0] else False
