from cantinaUtils.verify_login import verify_login
from flask import redirect, url_for, request, render_template


def add_modules_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        user_permission = database.select('''SELECT * from cantina_administration.permission WHERE user_token = %s''',
                                          (request.cookies.get('token')), 1)
        if not user_permission[27] and not user_permission[32]:  # Si l'utilisateur n'as pas la permission, redirection vers la page d'accueil
            return redirect(url_for('home'))

        if request.method == 'GET':
            return render_template('Administration/disabled_feature.html')
            # return render_template('Administration/modules/add_modules.html')

    elif verify_login(database) == 'desactivated':
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
