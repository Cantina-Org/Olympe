from cantinaUtils.verify_login import verify_login
from flask import request, render_template, redirect, url_for


def show_user_cogs(database):
    if verify_login(database):
        if request.args.get('user_token'):
            user_data = database.select('SELECT * FROM cantina_administration.user WHERE token = %s',
                                        (request.args.get('user_token')), number_of_data=1)
            return render_template('Administration/show_user.html', user_info=user_data, multiple_user_info=None)
        else:
            users_data = database.select('SELECT * FROM cantina_administration.user', None)
            return render_template('Administration/show_user.html', user_info=None, multiple_user_info=users_data)
    else:
        return redirect(url_for('sso_login'))
