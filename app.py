from flask import Flask, render_template
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, emit
import os 
import base64
import socket
from io import BytesIO
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
