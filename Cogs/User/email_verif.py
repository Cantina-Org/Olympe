from flask import request, render_template, redirect, url_for
from Utils.email_utils import send_verification_email
from Utils.verify_login import verify_login


def email_verif_cogs(database):
    if not verify_login(database):
        return redirect(url_for('sso_login', error='0'))
    elif verify_login(database) == 'desactivated':
        login_url = database.select('''SELECT fqdn FROM cantina_administration.modules WHERE name = 'Olympe' ''', None,
                                    number_of_data=1)[0]
        return redirect(login_url+'/sso/login/?error=2')

    if request.method == 'POST':
        code = request.form['mail-code']

        if code == database.select(
                '''SELECT email_verification_code FROM cantina_administration.user WHERE token = %s''',
                (request.cookies.get('token')), number_of_data=1)[0]:
            database.exec('''UPDATE cantina_administration.user SET email_verification_code = %s, email_verified = 1 
            WHERE token = %s''', ('checked', request.cookies.get('token')))
            return redirect(url_for('home'))
        else:
            return render_template('User/email-verif.html', error=1)

    elif request.method == 'GET':
        send_verification_email(database)
        return render_template('User/email-verif.html')
