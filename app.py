from flask import Flask, render_template
from flask_socketio import SocketIO
from cantinaUtils import Database
from os import path, getcwd
from json import load
from Cogs.SSO.login import sso_login_cogs
from Cogs.User.home import user_home_cogs

from Utils.devtools.create_user import create_user
from Utils.devtools.recreate_db import recreate_db

file_path = path.abspath(path.join(getcwd(), "config.json"))  # Trouver le chemin complet du fichier config.json

# Lecture du fichier JSON
with open(file_path, 'r') as file:
    config_data = load(file)  # Ouverture du fichier config.json

app = Flask(__name__)  # Création de l'application Flask
socketio = SocketIO(app)  # Lien entre l'application Flaks et le WebSocket

database = Database.DataBase(
    user=config_data['database'][0]['username'],
    password=config_data['database'][0]['password'],
    host=config_data['database'][0]['address'],
    port=config_data['database'][0]['port'],
    database='cantina_administration'
)  # Création de l'objet pour se connecter à la base de données via le module cantina
database.connection()  # Connexion à la base de données

database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.user(id INT PRIMARY KEY AUTO_INCREMENT, 
token TEXT NOT NULL,  username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, 
picture_id TEXT DEFAULT 'none', email_verified BOOL DEFAULT FALSE, email_verification_code TEXT, 
A2F BOOL DEFAULT FALSE, A2F_secret TEXT, last_connection DATE, admin BOOL DEFAULT FALSE, 
desactivated BOOL DEFAULT FALSE)""", None)
database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.config(id INT PRIMARY KEY AUTO_INCREMENT, 
name TEXT, content TEXT)""", None)
database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.modules(id INT PRIMARY KEY AUTO_INCREMENT, 
name TEXT, fqdn TEXT)""", None)
database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.permission(id INT PRIMARY KEY AUTO_INCREMENT,
user_token TEXT NOT NULL, show_log BOOL DEFAULT FALSE, edit_username BOOL DEFAULT FALSE, edit_email BOOL DEFAULT FALSE, 
edit_password BOOL DEFAULT FALSE, edit_profile_picture BOOL DEFAULT FALSE, edit_A2F BOOL DEFAULT FALSE, 
edit_ergo BOOL DEFAULT FALSE, show_specific_account BOOL DEFAULT FALSE, edit_username_admin BOOL DEFAULT FALSE,
edit_email_admin BOOL DEFAULT FALSE, edit_password_admin BOOL DEFAULT FALSE, 
edit_profile_picture_admin BOOl DEFAULT FALSE, allow_edit_username BOOL DEFAULT FALSE, 
allow_edit_email BOOL DEFAULT FALSE, allow_edit_password BOOL DEFAULT FALSE,
allow_edit_profile_picture BOOL DEFAULT FALSE, allow_edit_A2F BOOL DEFAULT FALSE, create_user BOOL DEFAULT FALSE, 
delete_account BOOL DEFAULT FALSE, desactivate_account BOOL DEFAULT FALSE, edit_permission BOOL DEFAULT FALSE, 
show_all_modules BOOL DEFAULT FALSE, on_off_modules BOOL DEFAULT FALSE, on_off_maintenance BOOL DEFAULT FALSE, 
delete_modules BOOL DEFAULT FALSE, add_modules BOOL DEFAULT FALSE)""", None)


# recreate_db(database)
# create_user(database, 'matyu', 'LeMdPDeTest', 'test@test.com', 1, 1)


@app.route('/', methods=['GET', 'POST'])
def home():
    return user_home_cogs(database)


@app.route('/sso/login/', methods=['GET', 'POST'])
def sso_login(error=0):
    return sso_login_cogs(database, error)


if __name__ == '__main__':
    socketio.run(app,
                 allow_unsafe_werkzeug=True,
                 debug=config_data["modules"][0]["debug_mode"],
                 port=config_data["modules"][0]["port"]
                 )
