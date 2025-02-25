from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import subprocess
import apigenerator
import configparser
from collections import deque

app = Flask(__name__)
socketio = SocketIO(app)

active_clients = set()
config = configparser.ConfigParser()
config.read('config.ini')

# Initialize a deque to store commands
command_queue = deque()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_api', methods=['POST'])
def generate_api():
    data = request.get_json()
    api_key = apigenerator.generate_api_key()
    return jsonify({'apikey': api_key})

@app.route('/verify_api', methods=['POST'])
def verify_api():
    api_key = request.headers.get("API-Key")
    if not api_key:
        return jsonify({'error': 'API key is missing'}), 401

    username = get_username_from_api_key(api_key)
    if not username:
        return jsonify({'error': 'Invalid API key'}), 401

    return jsonify({'status': 'API key is valid'})

@app.route('/set_command', methods=['POST'])
def set_command():
    data = request.get_json()
    command = data.get('command')
    print(command)
    command_queue.append(command)  # Add the command to the queue
    return jsonify({'status': 'Command added to queue'})

@app.route('/what2run', methods=['GET'])
def what2run():
    api_key = request.headers.get("API-Key")
    if not api_key:
        return jsonify({'error': 'API key is missing'}), 401

    username = get_username_from_api_key(api_key)
    if not username:
        return jsonify({'error': 'Invalid API key'}), 401

    if command_queue:
        command = command_queue.popleft()  # Remove and return the command from the queue
        return jsonify({'what2run': command})
    else:
        command = "None"
        
        return jsonify({'what2run': command})
  
    

def get_username_from_api_key(api_key):
    for username in config.sections():
        if config[username]['apikey'] == api_key:
            return username
    return None

@socketio.on('connect')
def handle_connect():
    active_clients.add(request.sid)
    emit('client_count', {'count': len(active_clients)}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    active_clients.discard(request.sid)
    emit('client_count', {'count': len(active_clients)}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)