from Utils.create_user import create_user
from Utils.verify_login import verify_login
from flask import redirect, url_for, request, render_template


def add_user_cogs(database):
    # Vérification de si l'utilisateur est bien connecté et n'a pas un compte désactivé
    if verify_login(database) and verify_login(database) != 'desactivated':
        # Si l'utilisateur n'a pas les permissions, redirection vers la page d'accueil
        if not database.select("""SELECT create_user FROM cantina_administration.permission WHERE user_token = %s""",
                               (request.cookies.get('token')), 1)[0]:
            return redirect(url_for('show_user'))

        if request.method == 'POST':  # Si il fait une requete de type POST
            _create_user = create_user(database)  # Création de l'utilisateur
            return redirect(url_for('show_user', user_token=_create_user))
        elif request.method == 'GET':  # Si il fait une requete de type GET
            return render_template('Administration/add_user.html')

    elif verify_login(database) == "desactivated":
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
