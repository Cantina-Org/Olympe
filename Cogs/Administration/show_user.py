from os import path

from cantinaUtils.verify_login import verify_login
from flask import request, render_template, redirect, url_for
from werkzeug.exceptions import BadRequestKeyError
from argon2 import PasswordHasher, exceptions
from werkzeug.utils import secure_filename


def show_user_cogs(database, upload_path):
    if verify_login(database):
        if request.method == 'GET':
            user_permission = database.select('''SELECT * FROM cantina_administration.permission 
            WHERE user_token = %s''', (request.cookies.get('token')), 1)
            if not user_permission[9]:
                return redirect(url_for('home'))

            if request.args.get('user_token'):
                user_data = database.select('SELECT * FROM cantina_administration.user WHERE token = %s',
                                            (request.args.get('user_token')), number_of_data=1)
                return render_template('Administration/show_user.html', user_info=user_data, multiple_user_info=None,
                                       user_permission=user_permission)
            else:
                users_data = database.select('SELECT * FROM cantina_administration.user', None)
                return render_template('Administration/show_user.html', user_info=None, multiple_user_info=users_data,
                                       user_permission=user_permission)
        elif request.method == 'POST':
            user_information = database.select("""SELECT * FROM cantina_administration.user WHERE token = %s""",
                                               (request.form['token']), 1)
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
                                  (PasswordHasher().hash(password=request.form['password1']),
                                   request.form['token']))
                else:
                    pass  # L'entrée est vide
            except BadRequestKeyError:
                pass  # Permission refusé

            try:
                if request.form['email'] != user_information[4]:
                    # Modification de l'email. Modification du code de verif & email_verified mis sur 0 car plus vérifié
                    database.exec('''UPDATE cantina_administration.user SET email = %s, email_verification_code = %s, 
                    email_verified = 0 WHERE token = %s''',
                                  (request.form['email'], 'reset', request.form['token']))
            except BadRequestKeyError:
                pass  # Permission refusé

            try:
                if request.form['theme'] != user_information[13]:
                    # Modification du theme si il est différent de celui déjà mis.
                    database.exec('''UPDATE cantina_administration.user SET theme = %s WHERE token = %s''',
                                  (request.form['theme'], request.form['token']))
            except BadRequestKeyError:
                pass  # Permission refusé

            if 'profile_picture' in request.files:
                profile_picture = request.files['profile_picture']
                if profile_picture.filename != '':
                    profile_picture.save(path.join(upload_path, secure_filename(request.form['token']) + '.' +
                                                   profile_picture.filename.rsplit('.', 1)[1].lower()))
                    database.exec('''UPDATE cantina_administration.user SET picture = 1 WHERE token = %s''',
                                  (request.form['token']))

            return redirect(url_for('show_user', user_token=request.form['token']))
        else:
            return redirect('https://i.pinimg.com/originals/cd/0d/76/cd0d7619041d1f141d3e6fea29bb2724.jpg')
    else:
        return redirect(url_for('sso_login'))
