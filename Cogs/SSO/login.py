from flask import request, render_template, redirect, url_for, make_response
from Utils.verify_login import verify_login
from argon2 import PasswordHasher


def sso_login_cogs(database, error):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        row = database.select("""SELECT password, token FROM cantina_administration.user WHERE username = %s""",
                              (username,), number_of_data=1)

        validation_code = database.select("""SELECT content FROM cantina_administration.config WHERE name=%s""",
                                          ('secret_token',), number_of_data=1)

        domain_to_redirect = database.select("""SELECT fqdn FROM cantina_administration.modules WHERE name=%s""",
                                             (request.args.get('modules'),), number_of_data=1)

        if row is None:  # Si aucune correspondance, redirect vers la page de login avec le message d'erreur n°1
            return redirect(url_for('sso_login', error='1'))
        else:
            match = PasswordHasher().verify(row[0], password)  # Verification de la correspondance du MDP

        if not match:  # Si le MDP correspond pas, redirect vers la page de login avec le message d'erreur n°1
            return redirect(url_for('sso_login', error='1'))
        else:
            if domain_to_redirect is None:
                response = make_response(redirect(url_for('home')))
            else:
                response = make_response(redirect(domain_to_redirect[0], code=302))
            # Création des cookies de vérification d'authentification
            response.set_cookie('token', row[1])
            response.set_cookie('validation', validation_code[0])
            return response

    elif request.method == 'GET':

        if verify_login(database):
            domain_to_redirect = database.select("""SELECT fqdn FROM cantina_administration.modules WHERE name=%s""",
                                                 (request.args.get('modules'),), number_of_data=1)

            if domain_to_redirect is None:
                return redirect(url_for('home'))
            else:
                return redirect(domain_to_redirect[0], code=302)

        return render_template('SSO/login.html', error=error)
