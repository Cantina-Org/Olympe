from Utils.verify_login import verify_login
from flask import redirect, url_for, request, render_template


def user_home_cogs(database):
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
        modules_info = database.select("""SELECT * FROM cantina_administration.modules""", None)
        nb_user = database.select("""SELECT COUNT(*) FROM cantina_administration.user""", None, number_of_data=1)[0]
        nb_module = database.select("""SELECT COUNT(*) FROM cantina_administration.modules""", None, number_of_data=1)[0]

        return render_template('User/index.html', user_information=user_information,
                               user_permission=user_permission, modules_info=modules_info, nb_user=nb_user, nb_module=nb_module)
