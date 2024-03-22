from Utils.verify_login import verify_login
from flask import redirect, url_for, request
from Utils.create_user import check_perm


def edit_user_permission_cogs(database):
    if verify_login(database) and verify_login(database) != 'desactivated':
        if (not database.select("""SELECT edit_permission FROM cantina_administration.permission 
        WHERE user_token = %s""", (request.cookies.get('token')), 1)[0]
                and request.cookies.get('token') != request.form['token']):
            return redirect(url_for('show_user'))

        database.exec('''UPDATE cantina_administration.permission SET show_log = %s, 
        edit_username = %s, edit_email = %s, edit_password = %s, edit_profile_picture = %s, edit_A2F = %s,
        edit_ergo = %s, show_specific_account = %s, edit_username_admin = %s, edit_email_admin = %s, 
        edit_password_admin = %s, edit_profile_picture_admin = %s, allow_edit_username = %s, allow_edit_email = %s, 
        allow_edit_password = %s, allow_edit_profile_picture = %s, allow_edit_A2F = %s, create_user = %s, 
        delete_account = %s, desactivate_account = %s, edit_permission = %s, show_all_modules = %s, on_off_modules = %s,
        on_off_maintenance = %s, delete_modules = %s, add_modules = %s WHERE user_token = %s''',
                      (check_perm('show-log'), check_perm('edit-username'), check_perm('edit-email'),
                       check_perm('edit-password'), check_perm('edit-profile-picture'), check_perm('edit-a2f'),
                       check_perm('edit-theme'), check_perm('show-all-user'), check_perm('edit-username-admin'),
                       check_perm('edit-email-admin'), check_perm('edit-password-admin'),
                       check_perm('edit-profile-picture-admin'), check_perm('allow-edit-username'),
                       check_perm('allow-edit-email'), check_perm('allow-edit-password'),
                       check_perm('allow-edit-profile-picture'), check_perm('allow-edit-a2f'), check_perm('create-user'),
                       check_perm('delete-user'), check_perm('desactivate-user'), check_perm('edit-user-permission'),
                       check_perm('show-all-modules'), check_perm('on-off-modules'), check_perm('on-off-maintenance'),
                       check_perm('delete-module'), check_perm('add-module'), request.form['token']))
        database.exec('''UPDATE cantina_administration.user SET admin = %s WHERE token=%s''', (check_perm('user-admin'),
                                                                                               request.form['token']))
        return redirect(url_for('show_user', user_token=request.form['token']))

    elif verify_login(database) == "desactivated":
        return redirect(url_for('sso_login', error='2'))
    else:
        return redirect(url_for('sso_login'))
