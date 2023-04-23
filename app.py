from json import load
from os import path, getcwd
from flask import Flask, request
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


@app.route('/')
def home():
    return home_cogs(request, database)


@app.route('/account/my', methods=['GET', 'POST'])
def my_account():
    return my_account_cogs(request, database)


@app.route('/login')
def auth():
    return login_cogs(request, database)


if __name__ == '__main__':
    app.run(port=config_data["port"])
