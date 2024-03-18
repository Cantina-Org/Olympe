def clear_log(database):
    database.exec("""DROP TABLE IF EXISTS cantina_administration.log""", None)
    database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.log(id INT PRIMARY KEY AUTO_INCREMENT, 
    action_name TEXT, user_ip TEXT, user_token TEXT, details TEXT, log_level INT)""", None)
