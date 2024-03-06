def recreate_db(database):
    database.exec("DROP TABLE IF EXISTS cantina_administration.user, cantina_administration.permission", None)
    database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.user(id INT PRIMARY KEY AUTO_INCREMENT, 
    token TEXT NOT NULL,  username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, 
    email_verified BOOL DEFAULT FALSE, email_verification_code TEXT, picture_id TEXT DEFAULT 'none',
    A2F BOOL DEFAULT FALSE, A2F_secret TEXT, last_connection DATE, admin BOOL DEFAULT FALSE, 
    desactivated BOOL DEFAULT FALSE)""", None)
    database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.permission(id INT PRIMARY KEY AUTO_INCREMENT,
    user_token TEXT NOT NULL, show_log BOOL DEFAULT FALSE, edit_username BOOL DEFAULT FALSE, 
    edit_email BOOL DEFAULT FALSE,edit_password BOOL DEFAULT FALSE, edit_profile_picture BOOL DEFAULT FALSE, 
    edit_A2F BOOL DEFAULT FALSE, edit_ergo BOOL DEFAULT FALSE, show_specific_account BOOL DEFAULT FALSE, 
    edit_username_admin BOOL DEFAULT FALSE, edit_email_admin BOOL DEFAULT FALSE, edit_password_admin BOOL DEFAULT FALSE, 
    edit_profile_picture_admin BOOl DEFAULT FALSE, allow_edit_username BOOL DEFAULT FALSE, 
    allow_edit_email BOOL DEFAULT FALSE, allow_edit_password BOOL DEFAULT FALSE,
    allow_edit_profile_picture BOOL DEFAULT FALSE, allow_edit_A2F BOOL DEFAULT FALSE, create_user BOOL DEFAULT FALSE, 
    delete_account BOOL DEFAULT FALSE, desactivate_account BOOL DEFAULT FALSE, edit_permission BOOL DEFAULT FALSE, 
    show_all_modules BOOL DEFAULT FALSE, on_off_modules BOOL DEFAULT FALSE, on_off_maintenance BOOL DEFAULT FALSE, 
    delete_modules BOOL DEFAULT FALSE, add_modules BOOL DEFAULT FALSE)""", None)
