from pyotp import random_base32, totp
from flask import request, render_template, redirect, url_for
from Utils.verify_login import verify_A2F, verify_login


def doubleFA_add_cogs(database):
    # Verification si l'utilisateur est connecté
    if not verify_login(database):
        return redirect(url_for('sso_login', error='0'))
    elif verify_login(database) == 'desactivated':  # Si l'utilisateur est connecté mais que son compte est désactivé
        login_url = database.select('''SELECT fqdn FROM cantina_administration.modules WHERE name = 'Olympe' ''', None,
                                    number_of_data=1)[0]
        return redirect(login_url+'/sso/login/?error=2')

    # On récupère les permissions de l'utilisateurs
    user_permission = database.select('''SELECT * from cantina_administration.permission WHERE user_token = %s''',
                                      (request.cookies.get('token')), 1)

    # On récupère les modules afin de pouvoir faire une redirection sur la page via la sidebar
    modules_info = database.select("""SELECT * FROM cantina_administration.modules""", None)

    # On récupère le thème de l'utilisateur afin de pouvoir l'afficher
    local_user_theme = database.select('''SELECT theme FROM cantina_administration.user WHERE token= %s''',
                                       (request.cookies.get('token')), 1)

    if request.method == 'POST':  # Si l'utilisateur valide le formulaire
        if verify_A2F(database):  # Vérification réussi du code via la base de donnée
            database.exec('''UPDATE cantina_administration.user SET A2F = 1 WHERE token=%s''',
                          (request.cookies.get('token')))  # Activation de l'A2F pour l'authentification
            return redirect(url_for('user_space'))
        else:  # Vérification raté du code
            # Génération du lien avec la chaine de caractère lié a l'utilisateur.
            key = database.select('''SELECT A2F_secret FROM cantina_administration.user WHERE token = %s''',
                                  (request.cookies.get('token')), number_of_data=1)[0]
            totp_auth = totp.TOTP(key).provisioning_uri(
                name='Cantina Olympe',
                issuer_name=database.select("""SELECT username FROM cantina_administration.user WHERE token = %s""",
                                            (request.cookies.get('token'),), number_of_data=1)[0]
            )
            return render_template('User/2FA-add.html', totp_auth=totp_auth,
                                   error=1, user_permission=user_permission, modules_info=modules_info, local_user_theme=local_user_theme)
    elif request.method == 'GET':  # Si l'utilisateur consulte la page du formulaire.
        # Si l'utilisateur à déjà l'A2F d'activé, redirection vers la page d'accueil.
        if database.select('''SELECT A2F FROM cantina_administration.user WHERE token=%s''',
                           (request.cookies.get('token')), number_of_data=1)[0]:
            return redirect(url_for('home'))

        # Si aucune chaine de caractère n'avait été généré
        if database.select('''SELECT A2F_secret FROM cantina_administration.user WHERE token = %s''',
                           (request.cookies.get('token')), number_of_data=1)[0] is None:
            key = random_base32()  # Génération d'une chaine de caractère unique
            database.exec("""UPDATE cantina_administration.user SET A2F_secret = %s WHERE token = %s""",
                          (key, request.cookies.get('token')))
        else:  # Sinon, la valeur de la base de données est séléctionné
            key = database.select('''SELECT A2F_secret FROM cantina_administration.user WHERE token = %s''',
                                  (request.cookies.get('token')), number_of_data=1)[0]

        # Génération du lien avec la chaine de caractère lié a l'utilisateur.
        totp_auth = totp.TOTP(key).provisioning_uri(
            name='Cantina Olympe',
            issuer_name=database.select("""SELECT username FROM cantina_administration.user WHERE token = %s""",
                                        (request.cookies.get('token'),), number_of_data=1)[0]
        )

        return render_template('User/2FA-add.html', totp_auth=totp_auth,
                               error=0, user_permission=user_permission, modules_info=modules_info, local_user_theme=local_user_theme)
