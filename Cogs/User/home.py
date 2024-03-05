from Utils.verify_login import verify_login
from flask import redirect, url_for, request, render_template


def user_home_cogs(database):
    if not verify_login(database):
        return redirect(url_for('sso_login', error='0'))

    if request.method == 'GET':
        return render_template('')
    elif request.method == 'POST':
        return "str"
        