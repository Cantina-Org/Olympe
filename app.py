from flask import Flask, render_template
from flask_socketio import SocketIO
from cantinaUtils import Database
from os import path, getcwd
from json import load
from Cogs.SSO.login import sso_login_cogs

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
token TEXT,  username TEXT, password TEXT, email TEXT, email_verified BOOL, email_verification_code TEXT, A2F BOOL, 
A2F_secret TEXT, last_connection DATE, admin BOOL, desactivated BOOL DEFAULT FALSE)""", None)
database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.config(id INT PRIMARY KEY AUTO_INCREMENT, 
name TEXT, content TEXT)""", None)
database.exec("""CREATE TABLE IF NOT EXISTS cantina_administration.modules(id INT PRIMARY KEY AUTO_INCREMENT, 
name TEXT, fqdn TEXT)""", None)

# recreate_db(database)
# create_user(database, 'matyu', 'LeMdPDeTest', 'test@test.com', 1, 1)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sso/login/', methods=['GET', 'POST'])
def sso_login(error=0):
    return sso_login_cogs(database, error)


if __name__ == '__main__':
    socketio.run(app,
                 allow_unsafe_werkzeug=True,
                 debug=config_data["modules"][0]["debug_mode"],
                 port=config_data["modules"][0]["port"]
                 )
