from Utils.create_user import create_user
from Utils.verify_login import verify_login
from flask import redirect, url_for, request, render_template


def add_user_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        if not database.select("""SELECT create_user FROM cantina_administration.permission WHERE user_token = %s""",
                               (request.cookies.get('token')), 1)[0]:
            return redirect(url_for('show_user'))

        if request.method == 'POST':
            _create_user = create_user(database)
            return redirect(url_for('show_user', user_token=_create_user))
        elif request.method == 'GET':
            return render_template('Administration/add_user.html')

    elif verify_login(database) == "desactivated":
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
