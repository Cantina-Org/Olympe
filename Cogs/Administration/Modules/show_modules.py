from cantinaUtils.verify_login import verify_login
from flask import redirect, url_for, request, render_template


def show_modules_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        user_permission = database.select('''SELECT * from cantina_administration.permission WHERE user_token = %s''',
                                          (request.cookies.get('token')), 1)
        if not user_permission[23]:  # Si l'utilisateur n'as pas la permission, redirection vers la page d'accueil
            return redirect(url_for('home'))

        if request.method == 'POST':
            try:
                if user_permission[28] and request.form["module_name"]:
                    edit_url = 1
            except Exception as e:
                print(e)
                edit_url = 0

            return redirect(url_for('show_modules'))
        else:
            if request.args.get('module_name'):
                module_info = database.select('''SELECT * FROM cantina_administration.modules WHERE name = %s''',
                                              (request.args.get('module_name')), 1)

                return render_template('Administration/show_one_modules.html', modules_info=module_info,
                                       user_permission=user_permission)
            else:
                modules_info = database.select('''SELECT * FROM cantina_administration.modules''', None)
            return render_template('Administration/show_modules.html', modules_info=modules_info)
    elif verify_login(database) == 'desactivated':
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
