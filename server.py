# server.py
# pip install flask flask-socketio

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
last_location = {}

@app.route('/')
def index():
    return "location server running"

@app.route('/request', methods=['POST'])
def request_location():
    # broadcast request to all connected clients
    socketio.emit('get_location', {'note': 'request from admin'})
    return jsonify({'status': 'sent'})

@app.route('/last', methods=['GET'])
def last():
    if not last_location:
        return jsonify({'status': 'no data'})
    return jsonify(last_location)

@socketio.on('location')
def handle_location(data):
    # data expected: { 'device': 'phone-b', 'coords': {...} }
    data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    last_location.clear()
    last_location.update(data)
    print('location received', last_location)

if __name__ == '__main__':
    # use Flask-SocketIO with threading (works fine on Windows)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)