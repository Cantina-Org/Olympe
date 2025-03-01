from uuid import uuid3, uuid1
from cantinaUtils.verify_login import verify_login
from flask import redirect, url_for, request, render_template


def add_modules_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        user_permission = database.select('''SELECT * from cantina_administration.permission WHERE user_token = %s''',
                                          (request.cookies.get('token')), 1)

        # On récupère les modules afin de pouvoir faire une redirection sur la page via la sidebar
        modules_info = database.select("""SELECT * FROM cantina_administration.modules""", None)

        # On récupère le thème de l'utilisateur afin de pouvoir l'afficher
        local_user_theme = database.select('''SELECT theme FROM cantina_administration.user WHERE token= %s''',
                                           (request.cookies.get('token')), 1)

        if not user_permission[27] and not user_permission[32]:  # Si l'utilisateur n'as pas la permission, redirection vers la page d'accueil
            return redirect(url_for('home'))

        if request.method == 'GET':
            # return render_template('Administration/disabled_feature.html')
            return render_template('Administration/modules/add_modules.html', user_permission=user_permission, local_user_theme=local_user_theme)
        elif request.method == 'POST':
            token = str(uuid3(uuid1(), str(uuid1())))  # Génération d'un token unique
            try:
                _maintenance = 1 if request.form["module_maintenance"] else 0
            except Exception as e:
                print(e)
                _maintenance = 0

            database.exec("""INSERT INTO cantina_administration.modules(token, name, fqdn, maintenance)
                VALUES (%s, %s, %s, %s)""", (token, request.form["module_name"], request.form["module_fqdn"], _maintenance))

            return redirect(url_for('show_modules', module_token=token))

    elif verify_login(database) == 'desactivated':
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
