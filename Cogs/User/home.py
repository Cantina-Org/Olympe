from Utils.verify_login import verify_login
from flask import redirect, url_for, request, render_template
from argon2 import PasswordHasher, exceptions
from werkzeug.exceptions import BadRequestKeyError
from werkzeug.utils import secure_filename
from os import path


def user_home_cogs(database, upload_path):
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
            if request.form['username'] != user_information[2]:
                # Modification de l'username après vérification qu'il ai changé
                database.exec('''UPDATE cantina_administration.user SET username = %s WHERE token = %s''',
                              (request.form['username'], request.cookies.get('token')))
        except BadRequestKeyError:
            pass  # Permission refusé

        try:
            if PasswordHasher().verify(user_information[3], request.form['password1']):
                pass  # Le MDP ne change pas
        except exceptions.VerifyMismatchError:
            if request.form['password1'] != '' and request.form['password1'] == request.form['password2']:
                # Modification du MDP après vérification que les deux entrées sont strictement égal et pas vides
                database.exec('''UPDATE cantina_administration.user SET password = %s WHERE token = %s''',
                              (PasswordHasher().hash(password=request.form['password1']), request.cookies.get('token')))
            else:
                pass  # L'entrée est vide
        except BadRequestKeyError:
            pass  # Permission refusé

        try:
            if request.form['email'] != user_information[4]:
                # Modification de l'email. Modification du code de verif et email_verified mis sur 0 car plus vérifié
                database.exec('''UPDATE cantina_administration.user SET email = %s, email_verification_code = %s, 
                email_verified = 0 WHERE token = %s''', (request.form['email'], '000000', request.cookies.get('token')))
        except BadRequestKeyError:
            pass  # Permission refusé

        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture.filename != '':
                profile_picture.save(path.join(upload_path, secure_filename(request.cookies.get('token')) + '.' +
                                               profile_picture.filename.rsplit('.', 1)[1].lower()))
                database.exec('''UPDATE cantina_administration.user SET picture = 1 WHERE token = %s''',
                              (request.cookies.get('token')))

        return redirect(url_for('home'))
        