from uuid import uuid3, uuid1
from argon2 import PasswordHasher
from Utils.verify_login import verify_login
from flask import redirect, url_for, request, render_template


def add_user_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        if not database.select("""SELECT create_user FROM cantina_administration.permission WHERE user_token = %s""",
                               (request.cookies.get('token')), 1)[0]:
            return redirect(url_for('show_user'))

        if request.method == 'POST':
            _create_user = create_user()
            return redirect(url_for('show_user', user_token=_create_user))
        elif request.method == 'GET':
            return render_template('Administration/add_user.html')

    elif verify_login(database) == "desactivated":
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))


def create_user(database, username, password, email, admin, show_log, edit_username, edit_email,
                edit_password, edit_profile_picture, edit_A2F, edit_ergo, show_specific_account, edit_username_admin,
                edit_email_admin, edit_password_admin, edit_profile_picture_admin, allow_edit_username,
                allow_edit_email, allow_edit_password, allow_edit_profile_picture, allow_edit_A2F, create_user,
                delete_account, desactivate_account, edit_permission,  show_all_modules, on_off_modules,
                on_off_maintenance, delete_modules, add_modules):

    token = str(uuid3(uuid1(), str(uuid1())))
    hashed_password = PasswordHasher().hash(password)

    database.exec("""INSERT INTO cantina_administration.user(token, username, password, email, admin) 
    VALUES (%s, %s, %s, %s, %s)""", (token, username, hashed_password, email, admin))

    database.exec("""INSERT INTO cantina_administration.permission(user_token, show_log, edit_username, edit_email, 
    edit_password, edit_profile_picture, edit_A2F, edit_ergo, show_specific_account, edit_username_admin, 
    edit_email_admin, edit_password_admin, edit_profile_picture_admin, allow_edit_username, allow_edit_email, 
    allow_edit_password, allow_edit_profile_picture, allow_edit_A2F, create_user, delete_account, desactivate_account, 
    edit_permission, show_all_modules, on_off_modules, on_off_maintenance, delete_modules, add_modules) VALUES (%s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)""",
                  (token, show_log, edit_username, edit_email, edit_password, edit_profile_picture, edit_A2F, edit_ergo,
                   show_specific_account, edit_username_admin, edit_email_admin, edit_password_admin,
                   edit_profile_picture_admin, allow_edit_username, allow_edit_email, allow_edit_password,
                   allow_edit_profile_picture, allow_edit_A2F, create_user, delete_account, desactivate_account,
                   edit_permission, show_all_modules, on_off_modules, on_off_maintenance, delete_modules, add_modules))

    return token