from uuid import uuid3, uuid1
from werkzeug.exceptions import BadRequestKeyError
from argon2 import PasswordHasher
from flask import request


def create_user(database):
    token = str(uuid3(uuid1(), str(uuid1())))  # Génération d'un token unique
    hashed_password = PasswordHasher().hash(request.form['password-1'])  # Hashage des mots de passe

    # Création de l'utilisateur dans la base de données
    database.exec("""INSERT INTO cantina_administration.user(token, username, password, email, admin) 
    VALUES (%s, %s, %s, %s, %s)""", (token, request.form['username'], hashed_password, request.form['email'],
                                     check_perm('user-admin')))

    # Création des permissions de l'utilisateur dans la base de données
    database.exec("""INSERT INTO cantina_administration.permission(user_token, show_log, edit_username, edit_email, 
    edit_password, edit_profile_picture, edit_A2F, edit_ergo, show_specific_account, edit_username_admin, 
    edit_email_admin, edit_password_admin, edit_profile_picture_admin, allow_edit_username, allow_edit_email, 
    allow_edit_password, allow_edit_profile_picture, allow_edit_A2F, create_user, delete_account, desactivate_account, 
    edit_permission, show_all_modules, on_off_modules, on_off_maintenance, delete_modules, add_modules, 
    edit_smtp_config, edit_socket_url, edit_url_module, edit_name_module) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)""",
                  (token,
                   check_perm('show-log'), check_perm('edit-username'), check_perm('edit-email'),
                   check_perm('edit-password'), check_perm('edit-profile-picture'), check_perm('edit-a2f'),
                   check_perm('edit-theme'), check_perm('show-all-user'), check_perm('edit-username-admin'),
                   check_perm('edit-email-admin'), check_perm('edit-password-admin'),
                   check_perm('edit-profile-picture-admin'), check_perm('allow-edit-username'),
                   check_perm('allow-edit-email'), check_perm('allow-edit-password'),
                   check_perm('allow-edit-profile-picture'), check_perm('allow-edit-a2f'), check_perm('create-user'),
                   check_perm('delete-user'), check_perm('desactivate-user'), check_perm('edit-user-permission'),
                   check_perm('show-all-modules'), check_perm('on-off-modules'), check_perm('on-off-maintenance'),
                   check_perm('delete-module'), check_perm('add-module'), check_perm('edit-module-name'),
                   check_perm('edit-module-url'), check_perm('edit-socket-url'), check_perm('edit-smtp-config')))

    return token


def check_perm(perm_name):
    try:
        return 1 if request.form[perm_name] else 0  # Vérifie si perm_name existe dans le formulaire.
    except BadRequestKeyError:
        return 0
