from cantinaUtils.verify_login import verify_login
from flask import redirect, url_for, request
from json import dump

import app


def maintenance_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        user_permission = database.select('''SELECT * from cantina_administration.permission WHERE user_token = %s''',
                                          (request.cookies.get('token')), 1)

        if not user_permission[23] and not user_permission[32]:  # Si l'utilisateur n'as pas la permission, redirection vers la page d'accueil
            return redirect(url_for('home'))

        if request.method == 'POST':
            print(app.config_data['modules'][0]['maintenance'])
            app.config_data['modules'][0]['maintenance'] = not app.config_data['modules'][0]['maintenance']
            print(app.config_data['modules'][0]['maintenance'])

            with open(app.file_path, 'w') as file:
                dump(app.config_data, file, indent=4)

            return redirect(url_for('show_modules', module_name=request.form["module_name"]))

    elif verify_login(database) == 'desactivated':
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
