from flask import Flask, render_template
from flask_socketio import SocketIO, send
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('run_command')
def handle_run_command(data):
    command = data['command']
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    socketio.emit('terminal_output', {'data': output})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000, allow_unsafe_werkzeug=True)
