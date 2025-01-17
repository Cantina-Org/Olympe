from flask import Flask
from flask_socketio import SocketIO
from cantinaUtils import Database
from os import path, getcwd
from json import load

from Cogs.SSO.login import sso_login_cogs
from Cogs.SSO.logout import sso_logout_cogs
from Cogs.User.home import user_home_cogs
from Cogs.User.user_space import user_space_cogs
from Cogs.User.doublefa_add import doubleFA_add_cogs
from Cogs.User.email_verif import email_verif_cogs
from Cogs.Administration.User.show_user import show_user_cogs
from Cogs.Administration.User.desactivate_user import desactivate_user_cogs
from Cogs.Administration.User.delete_user import delete_user_cogs
from Cogs.Administration.User.add_user import add_user_cogs
from Cogs.Administration.User.edit_user_permission import edit_user_permission_cogs
from Cogs.Administration.User.global_permission import global_permission_cogs
from Cogs.Administration.User.smtp_config import smtp_config_cogs
from Cogs.Administration.Modules.show_modules import show_modules_cogs
from Cogs.Administration.Modules.add_modules import add_modules_cogs

file_path = path.abspath(path.join(getcwd(), "config.json"))  # Trouver le chemin complet du fichier config.json

# Lecture du fichier JSON
with open(file_path, 'r') as file:
    config_data = load(file)  # Ouverture du fichier config.json

app = Flask(__name__)  # Création de l'application Flask
socketio = SocketIO(app)  # Lien entre l'application Flaks et le WebSocket
app.config['UPLOAD_FOLDER'] = path.abspath(path.join(getcwd(), "static/ProfilePicture/"))
app.config['SERVER_NAME'] = config_data['modules'][0]['global_domain']

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
picture BOOL DEFAULT false, email_verified BOOL DEFAULT FALSE, email_verification_code TEXT, 
A2F BOOL DEFAULT FALSE, A2F_secret TEXT, last_connection DATE, admin BOOL DEFAULT FALSE, 
desactivated BOOL DEFAULT FALSE, theme TEXT DEFAULT 'white')""", None)
database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.config(id INT PRIMARY KEY AUTO_INCREMENT, 
name TEXT, content TEXT)""", None)
database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.modules(id INT PRIMARY KEY AUTO_INCREMENT, 
token TEXT, name TEXT, fqdn TEXT, maintenance BOOL default FALSE, status INTEGER DEFAULT 0, 
socket_url TEXT DEFAULT '/socket/')""", None)
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
delete_modules BOOL DEFAULT FALSE, add_modules BOOL DEFAULT FALSE, edit_name_module BOOL DEFAULT FALSE, 
edit_url_module BOOL DEFAULT FALSE, edit_socket_url BOOL DEFAULT FALSE, edit_smtp_config BOOL DEFAULT FALSE)""", None)
database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.log(id INT PRIMARY KEY AUTO_INCREMENT, 
    action_name TEXT, user_ip TEXT, user_token TEXT, details TEXT, log_level INT)""", None)


@app.route('/', methods=['GET'])
def home():
    return user_home_cogs(database)


@app.route('/user_space/', methods=['GET', 'POST'])
def user_space():
    return user_space_cogs(database, app.config['UPLOAD_FOLDER'])


@app.route('/2FA/add/', methods=['GET', 'POST'])
def double2FA_add():
    return doubleFA_add_cogs(database)


@app.route('/email/verif/', methods=['GET', 'POST'])
def email_verif():
    return email_verif_cogs(database)


"""
    Partie administration
"""


@app.route('/admin/user/', methods=['GET', 'POST'])
def show_user():
    return show_user_cogs(database, app.config['UPLOAD_FOLDER'])


@app.route('/admin/user/add/', methods=['GET', 'POST'])
def add_user():
    return add_user_cogs(database)


@app.route('/admin/user/edit_permission/', methods=['POST'])
def edit_permission_user():
    return edit_user_permission_cogs(database)


@app.route('/admin/user/desactivate/', methods=['POST'])
def desactivate_user():
    return desactivate_user_cogs(database)


@app.route('/admin/user/delete/', methods=['POST'])
def delete_user():
    return delete_user_cogs(database)


@app.route('/admin/permission/global/', methods=['POST', 'GET'])
def global_permission():
    return global_permission_cogs(database)


@app.route('/admin/modules/', methods=['POST', 'GET'])
def show_modules():
    return show_modules_cogs(database)


@app.route('/admin/modules/add/', methods=['POST', 'GET'])
def add_modules():
    return add_modules_cogs(database)


@app.route('/admin/smtp/config/', methods=['POST', 'GET'])
def smtp_config():
    return smtp_config_cogs(database)


"""
    Partie Single Sign On
"""


@app.route('/sso/login/', methods=['GET', 'POST'])
def sso_login(error=0):
    return sso_login_cogs(database, error, app.config['SERVER_NAME'])

@app.route('/sso/logout/', methods=['GET'])
def sso_logout():
    return sso_logout_cogs()


if __name__ == '__main__':
    socketio.run(app,
                 allow_unsafe_werkzeug=True,
                 debug=config_data["modules"][0]["debug_mode"],
                 port=config_data["modules"][0]["port"]
                 )
