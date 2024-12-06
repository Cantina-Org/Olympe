from flask_socketio import emit

def heart_beat_cogs(data):
    print(data)
    emit('response', {"data": "CACAAAAA"})