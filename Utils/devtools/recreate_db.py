def recreate_db(database):
    database.exec("DROP TABLE IF EXISTS cantina_administration.user", None)
    database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.user(id INT PRIMARY KEY AUTO_INCREMENT, 
token TEXT NOT NULL,  username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, 
email_verified BOOL DEFAULT FALSE, email_verification_code TEXT, picture_id TEXT DEFAULT 'none',
A2F BOOL DEFAULT FALSE, A2F_secret TEXT, last_connection DATE, admin BOOL DEFAULT FALSE, 
desactivated BOOL DEFAULT FALSE)""", None)
