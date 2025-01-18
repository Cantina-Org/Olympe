from flask import request, render_template, redirect, url_for
from Utils.verify_login import verify_login

def verify_maintenance(database, maintenance):
    if not request.path.startswith('/static/') and not request.path.startswith('/sso/'):
        if not verify_login(database):
            return redirect(url_for('sso_login', error='0'))
        else:
            user_permission = database.select("""SELECT admin FROM cantina_administration.permission WHERE user_token=%s""",
                                              (request.cookies.get('token')), 1)
            if maintenance and not user_permission[0]:
                return render_template("User/maintenance.html")
            elif maintenance and user_permission[0]:
                pass
            else:
                pass
    else:
        pass
