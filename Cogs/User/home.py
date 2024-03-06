from Utils.verify_login import verify_login
from flask import redirect, url_for, request, render_template
from argon2 import PasswordHasher, exceptions
from werkzeug.exceptions import BadRequestKeyError


def user_home_cogs(database):
    if not verify_login(database):
        return redirect(url_for('sso_login', error='0'))

    user_information = database.select("""SELECT * FROM cantina_administration.user WHERE token = %s""",
                                       (request.cookies.get('token')), 1)

    if request.method == 'GET':
        user_permission = database.select("""SELECT * FROM cantina_administration.permission WHERE user_token = %s""",
                                          (request.cookies.get('token')), 1)

        return render_template('Administration/index.html', user_information=user_information,
                               user_permission=user_permission)

    elif request.method == 'POST':
        try:
            if request.form['username'] and request.form['username'] != user_information[2]:
                database.exec('''UPDATE cantina_administration.user SET username = %s WHERE token = %s''',
                              (request.form['username'], request.cookies.get('token')))
        except BadRequestKeyError:
            print('Permission non accordé !')

        try:
            if PasswordHasher().verify(user_information[3], request.form['password1']):
                print('Le mot de passe ne change pas !')
        except exceptions.VerifyMismatchError:
            if request.form['password1'] != '' and request.form['password1'] == request.form['password2']:
                database.exec('''UPDATE cantina_administration.user SET password = %s WHERE token = %s''',
                              (PasswordHasher().hash(password=request.form['password1']), request.cookies.get('token')))
            else:
                print('Le champs est vide !')
        except BadRequestKeyError:
            print('Permission non accordé !')

        try:
            if request.form['email'] != user_information[4]:
                database.exec('''UPDATE cantina_administration.user SET email = %s, email_verification_code = %s, 
                email_verified = %s WHERE token = %s''', (request.form['email'], '000000', 0,
                                                          request.cookies.get('token')))
        except BadRequestKeyError:
            print('Permission non accordé !')
        return redirect(url_for('home'))
        