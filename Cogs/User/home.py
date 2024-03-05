from Utils.verify_login import verify_login
from flask import redirect, url_for, request, render_template
from argon2 import PasswordHasher, exceptions


def user_home_cogs(database):
    if not verify_login(database):
        return redirect(url_for('sso_login', error='0'))

    user_information = database.select("""SELECT * FROM cantina_administration.user WHERE token = %s""",
                                       (request.cookies.get('token')), number_of_data=1)

    if request.method == 'GET':
        return render_template('Administration/index.html', user_information=user_information)
    elif request.method == 'POST':
        if request.form['username'] != user_information[2]:
            database.exec('''UPDATE cantina_administration.user SET username = %s WHERE token = %s''',
                          (request.form['username'], request.cookies.get('token')))
        try:
            if PasswordHasher().verify(user_information[3], request.form['password']):
                print('Le mot de passe ne change pas !')
        except exceptions.VerifyMismatchError:
            if request.form['password'] != '':
                database.exec('''UPDATE cantina_administration.user SET password = %s WHERE token = %s''',
                              (PasswordHasher().hash(password=request.form['password']), request.cookies.get('token')))
            else:
                print('Le champs est vide !')

        if request.form['email'] != user_information[4]:
            database.exec('''UPDATE cantina_administration.user SET email = %s, email_verification_code = %s, 
            email_verified = %s WHERE token = %s''', (request.form['email'], '000000', 0, request.cookies.get('token')))

        return redirect(url_for('home'))
        