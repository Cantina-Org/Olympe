from flask import request, render_template, redirect, url_for
from argon2 import PasswordHasher


def sso_login_cogs(database, error):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(username, password)

        row = database.exec("""SELECT password, token FROM cantina_administration.user WHERE username = %s LIMIT 1""",
                            (username,))

        print(row)

        if row is None:
            return redirect(url_for('sso_login', error='1'))
        else:
            match = PasswordHasher().verify(row[0], password)

        return str(match)
    elif request.method == 'GET':
        return render_template('SSO/login.html', error=error)
