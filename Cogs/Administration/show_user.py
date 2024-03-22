from os import path
from Utils.verify_login import verify_login
from flask import request, render_template, redirect, url_for
from werkzeug.exceptions import BadRequestKeyError
from argon2 import PasswordHasher, exceptions
from werkzeug.utils import secure_filename


def show_user_cogs(database, upload_path):
    # Vérification de si l'utilisateur est bien connecté et n'a pas un compte désactivé
    if verify_login(database) and verify_login(database) != "desactivated":
        if request.method == 'GET':  # Si il fait une requete de type GET
            user_permission = database.select('''SELECT * FROM cantina_administration.permission 
            WHERE user_token = %s''', (request.cookies.get('token')), 1)  # On prend les permissions de l'utilsateur
            if not user_permission[9]:  # Si l'utilisateur n'a pas les permissions, redirection vers la page d'accueil
                return redirect(url_for('home'))

            # Si l'utilisateur souhaite voir un utilisateur en particulier
            if request.args.get('user_token'):
                # Sélectionne les données et permissions de l'utilisateur souhaité
                user_data = database.select('SELECT * FROM cantina_administration.user WHERE token = %s',
                                            (request.args.get('user_token')), number_of_data=1)
                selected_user_permission = database.select('''SELECT * FROM cantina_administration.permission WHERE 
                user_token = %s''', (request.args.get('user_token')), number_of_data=1)

                return render_template('Administration/show_user.html', user_info=user_data, multiple_user_info=None,
                                       user_permission=user_permission,
                                       selected_user_permission=selected_user_permission)
            else:  # Sinon, on séléctionne toute la base de données
                users_data = database.select('SELECT * FROM cantina_administration.user', None)
                return render_template('Administration/show_user.html', user_info=None, multiple_user_info=users_data,
                                       user_permission=user_permission, selected_user_permission=None)
        elif request.method == 'POST':  # Si l'utilisateur fait une requete POST
            user_information = database.select("""SELECT * FROM cantina_administration.user WHERE token = %s""",
                                               (request.form['token']), 1)
            try:
                if request.form['username'] != user_information[2]:  # Vérification que le username ai changé
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

            if 'profile_picture' in request.files:  # Si une photo de profile a été envoyé
                profile_picture = request.files['profile_picture']  # Récupération de la photo
                if profile_picture.filename != '':
                    # Sauvegarde de la photo
                    profile_picture.save(path.join(upload_path, secure_filename(request.form['token']) + '.' +
                                                   profile_picture.filename.rsplit('.', 1)[1].lower()))
                    # Modification dans la base de données pour pouvoir utiliser la photo.
                    database.exec('''UPDATE cantina_administration.user SET picture = 1 WHERE token = %s''',
                                  (request.form['token']))

            return redirect(url_for('show_user', user_token=request.form['token']))
        else:  # Si l'utilisateur utilise un autre moyen d'acceder à la page, un easter egg apparait
            return redirect('https://i.pinimg.com/originals/cd/0d/76/cd0d7619041d1f141d3e6fea29bb2724.jpg')
    elif verify_login(database) == "desactivated":
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
