from Utils.verify_login import verify_login
from flask import redirect, url_for, request, jsonify
from Utils.Administration.User.create_user import check_perm


def edit_user_permission_cogs(database):
    # Verify if user is logged in and account is not deactivated
    if verify_login(database) and verify_login(database) != 'desactivated':
        # Check if user has permission to edit permissions
        if (not database.select("""SELECT edit_permission FROM cantina_administration.permission 
                WHERE user_token = %s""", (request.cookies.get('token')), 1)[0]
                and request.cookies.get('token') != request.form['token']):
            return redirect(url_for('show_user'))

        if request.json['permission_name'] != "user_admin":
            database.exec(f'''UPDATE cantina_administration.permission SET {request.json['permission_name']} = %s 
            WHERE user_token = %s''', (request.json['value'], request.json['token']))
        else:
            database.exec(f'''UPDATE cantina_administration.user SET admin=%s WHERE token = %s''',
                          (request.json['value'], request.json['token']))

        return jsonify({"uuid":"caca"})

    elif verify_login(database) == "desactivated":
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))