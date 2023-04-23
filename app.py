from json import load
from os import path, getcwd
from flask import Flask, request

from Cogs.admin.add_user import add_user_cogs
from Cogs.admin.home import home_admin_cogs
from Cogs.admin.show_log import show_log_cogs
from Cogs.admin.show_user import show_user_cogs
from Cogs.home import home_cogs
from Cogs.login import login_cogs
from Cogs.my_account import my_account_cogs
from Utils.database import DataBase

app = Flask(__name__)
conf_file = open(path.abspath(getcwd()) + "/config.json", 'r')
config_data = load(conf_file)

# Connection aux bases de données
database = DataBase(user=config_data['database'][0]['database_username'],
                    password=config_data['database'][0]['database_password'], host="localhost", port=3306)
database.connection()


# Creation des tables des bases données
database.create_table(
    "CREATE TABLE IF NOT EXISTS cantina_administration.user(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, token TEXT,  "
    "user_name TEXT, salt TEXT, password TEXT, admin BOOL, work_Dir TEXT, last_online TEXT)")
database.create_table(
    "CREATE TABLE IF NOT EXISTS cantina_administration.log(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name TEXT,  "
    "user_ip text, user_token TEXT, argument TEXT, log_level INT, date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
database.create_table(
    "CREATE TABLE IF NOT EXISTS cantina_administration.file_sharing(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, "
    "file_name TEXT, file_owner text, file_short_name TEXT, login_to_show BOOL DEFAULT 1, password TEXT, "
    "date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
database.create_table(
    "CREATE TABLE IF NOT EXISTS cantina_administration.api(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, token TEXT, "
    "api_name TEXT, api_desc TEXT, owner TEXT)")
database.create_table(
    "CREATE TABLE IF NOT EXISTS cantina_administration.api_permission(token_api TEXT, create_file BOOL, upload_file "
    "BOOL, delete_file BOOL, create_folder BOOL, delete_folder BOOL, share_file_and_folder BOOL, "
    "delete_share_file_and_folder BOOL, create_user BOOL, delete_user BOOL)")


@app.route('/')
def home():
    return home_cogs(request, database)


@app.route('/account/my', methods=['GET', 'POST'])
def my_account():
    return my_account_cogs(request, database)


@app.route('/login')
def auth():
    return login_cogs(request, database)


# Fonction permettant de voire la page 'principale' du panel Admin de Cantina Cloud
@app.route('/admin/home')
def admin_home():
    return home_admin_cogs(request, database)


# Fonction permettant de visualiser les utilisateur de Cantina Cloud
@app.route('/admin/usermanager/')
@app.route('/admin/usermanager/<user_name>')
def admin_show_user(user_name=None):
    return show_user_cogs(request, database, user_name)


# Fonction permettant de créer un utilisateur
@app.route('/admin/add_user/', methods=['POST', 'GET'])
def admin_add_user():
    return add_user_cogs(request, database)


# Fonction permettant de voire les logs générer par Cantina Cloud
@app.route('/admin/show_log/')
@app.route('/admin/show_log/<log_id>')
def admin_show_log(log_id=None):
    return show_log_cogs(request, database, log_id)


if __name__ == '__main__':
    app.run(port=config_data["port"])
