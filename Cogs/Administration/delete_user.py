from Utils.verify_login import verify_login
from flask import redirect, url_for, request


def delete_user_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        if not database.select("""SELECT delete_account FROM cantina_administration.permission 
        WHERE user_token = %s""", (request.form['token_action_author']), 1)[0]:
            return redirect(url_for('show_user'))

        database.exec('''DELETE FROM cantina_administration.user WHERE token = %s''',
                      (request.form['token_to_delete']))
        database.exec('''DELETE FROM cantina_administration.permission WHERE user_token = %s''',
                      (request.form['token_to_delete']))
        return redirect(url_for('show_user'))

    elif verify_login(database) == "desactivated":
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
