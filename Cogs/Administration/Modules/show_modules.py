from cantinaUtils.verify_login import verify_login
from flask import redirect, url_for, request, render_template


def show_modules_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        if request.method == 'POST':
            return 'ziziizizizizii'
        else:
            if request.args.get('module_name'):
                module_info = database.select('''SELECT * FROM cantina_administration.modules WHERE name = %s''',
                                              (request.args.get('module_name')), 1)

                return render_template('Administration/show_one_modules.html', modules_info=module_info)
            else:
                modules_info = database.select('''SELECT * FROM cantina_administration.modules''', None)
            return render_template('Administration/show_modules.html', modules_info=modules_info)
    elif verify_login(database) == 'desactivated':
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
