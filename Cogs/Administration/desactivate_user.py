from Utils.verify_login import verify_login
from flask import redirect, url_for, request


def desactivate_user_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        if not database.select("""SELECT desactivate_account FROM cantina_administration.permission 
        WHERE user_token = %s""", (request.form['token_action_author']), 1)[0]:
            return redirect(url_for('show_user'))

        database.exec('''UPDATE cantina_administration.user SET desactivated = 1 WHERE token = %s''',
                      (request.form['token_to_desactivate']))
        return redirect(url_for('show_user', user_token=request.form['token_to_desactivate']))

    elif verify_login(database) == "desactivated":
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
