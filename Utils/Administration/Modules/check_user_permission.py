from flask import request


def has_user_permission(database, db_name, perm_name):
    return 1 if database.select(f'''SELECT {perm_name} FROM {db_name}.permission WHERE user_token=%s''', (
        request.cookies.get('token'))) else 0  # Vérifie si perm_name existe dans le formulaire.

