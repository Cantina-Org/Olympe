from flask_socketio import emit
from time import time

def heart_beat_cogs(data, database):
    print(data["date"])

    fqdn_data = database.select('''SELECT * from cantina_administration.modules WHERE token = %s''', (data['token']), 1)

    if fqdn_data[3] == data["fqdn"] and fqdn_data[1] == data["token"]:
        print('ICI')
        database.exec('''UPDATE cantina_administration.modules SET last_heartbeat = %s AND status = 1
                        WHERE token = %s''', (data['date'], data['token']))
        print(data['date'], data['token'])

    emit('response-heartbeat', {"receive-at": round(time())})