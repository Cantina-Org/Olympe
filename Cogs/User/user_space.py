from Utils.verify_login import verify_login
from flask import redirect, url_for, request, render_template
from argon2 import PasswordHasher, exceptions
from werkzeug.exceptions import BadRequestKeyError
from werkzeug.utils import secure_filename
from os import path, remove


def user_space_cogs(database, upload_path):
    # Verification si l'utilisateur est connecté
    if not verify_login(database):
        return redirect(url_for('sso_login', error='0'))
    elif verify_login(database) == 'desactivated':  # Si l'utilisateur est connecté mais que son compte est désactivé
        login_url = database.select('''SELECT fqdn FROM cantina_administration.modules WHERE name = 'olympe' ''', None,
                                    number_of_data=1)[0]
        return redirect(login_url+'/sso/login/?error=2')

    # Récupération des données de l'utilisateur
    user_information = database.select("""SELECT * FROM cantina_administration.user WHERE token = %s""",
                                       (request.cookies.get('token')), 1)

    if request.method == 'GET':
        # Récupération des permission de l'utilisateur
        user_permission = database.select("""SELECT * FROM cantina_administration.permission WHERE user_token = %s""",
                                          (request.cookies.get('token')), 1)
        # On récupère les modules afin de pouvoir faire une redirection sur la page via la sidebar
        modules_info = database.select("""SELECT * FROM cantina_administration.modules""", None)

        return render_template('User/user_space.html', user_information=user_information,
                               user_permission=user_permission, modules_info=modules_info)

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
                pass  # Le MDP ne change pas.
        except exceptions.VerifyMismatchError:
            if request.form['password1'] != '' and request.form['password1'] == request.form['password2']:
                # Modification du MDP après vérification que les deux entrées sont strictement égal et pas vides
                database.exec('''UPDATE cantina_administration.user SET password = %s WHERE token = %s''',
                              (PasswordHasher().hash(password=request.form['password1']), request.cookies.get('token')))
            else:
                pass  # L'entrée est vide.
        except BadRequestKeyError:
            pass  # Permission refusé

        try:
            if request.form['email'] != user_information[4]:
                # Modification de l'email. Modification du code de verif et email_verified mis sur 0 car plus vérifié
                database.exec('''UPDATE cantina_administration.user SET email = %s, email_verification_code = %s, 
                email_verified = 0 WHERE token = %s''', (request.form['email'], 'reset', request.cookies.get('token')))
        except BadRequestKeyError:
            pass  # Permission refusé

        try:
            if request.form['theme'] != user_information[12]:
                # Modification du theme s'il est différent de celui déjà mis.
                database.exec('''UPDATE cantina_administration.user SET theme = %s WHERE token = %s''',
                              (request.form['theme'], request.cookies.get('token')))
        except BadRequestKeyError:
            pass  # Permission refusé

        if 'profile_picture' in request.files:  # Si une photo de profile a été envoyé
            profile_picture = request.files['profile_picture']  # Récupération de la photo
            if profile_picture.filename != '':
                # Supression des autres photos de profile
                for extension in ['png', 'jpg', 'jpeg', 'heic']:
                    filepath = path.join(upload_path, f"{request.cookies.get('token')}.{extension}")
                    if path.exists(filepath):
                        remove(filepath)

                # Sauvegarde de la photo
                profile_picture.save(path.join(upload_path, secure_filename(request.cookies.get('token')) + '.' +
                                               profile_picture.filename.rsplit('.', 1)[1].lower()))
                # Modification dans la base de données pour pouvoir utiliser la photo.
                database.exec('''UPDATE cantina_administration.user SET picture = 1 WHERE token = %s''',
                              (request.cookies.get('token')))

        return redirect(url_for('user_space'))
        