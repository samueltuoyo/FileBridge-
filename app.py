from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, emit
import os 
import base64
import socket
from io import BytesIO

app = Flask(__name__)
#  This is the config 
app.config["SECRET_KEY"] = 'This is my Secret Key'
app.config["SESSION_TYPE"] = 'filesystem'

# This Host is to get the host IP address of the current machine 
host = "192.168.221.1"

Session(app)

DOWNLOAD = os.path.join(app.root_path, 'uploaded_files')
os.makedirs(DOWNLOAD, exist_ok=True)

SocketIO = SocketIO(app, manage_session=False)
# These are the routes for the url and radiation page 
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/sender', methods=["GET", "POST"])
def sender():
    # This will check for a post methods 
    if (request.method == "POST"):
        username: str = request.form["username"]
        room_name: str = request.form["Room_Name"]
     # This code will store the session incase the user close 
     # the tab or open a new tab
        session["username"] = username
        session["Room_Name"] = room_name
        return render_template('share/sender.html', Session=session)
    # Else the user is already logged in and the client is already in a room it will redirect back to the room 
    else: 
        # Handle logged in users
        if (session.get('username') is not None):
            return render_template('share/receiver.html', Session=session)
        else:
            return redirect(url_for('receiver'))

@app.route('/receiver', methods=["GET", "POST"])
def receiver():
    return render_template('share/receiver.html')

@app.route('/download_temp/<file_name>')
def download_temp_file(file_name):
    file_data = request.args.get('file_data')
    file_bytes = base64.b64decode(file_data.split(",")[1])
    file_stream = BytesIO(file_bytes)
    file_stream.seek(0)
    return send_file(file_stream, as_attachment=True, download_name=file_name)


@app.route('/instructions')
def instructions():
    return render_template('instructions/instructions.html')

@app.route('/mp3')
def to_mp3():
    return render_template('To-mp3/video-to-mp3.html')

# This is the code for the socketIO connection 

@SocketIO.on('sender',  namespace='/sender')
def sender(message):
    Room_Name: str = session.get('Room_Name')
    username: str = session.get('username')
    join_room(room=Room_Name)
    emit('status', {
        "msg": f"{username} has joined the room!!! "
    }, room=Room_Name)


@SocketIO.on("text", namespace="/sender")
def text(message):
    Room_Name = session.get("room_name")
    username = session.get("username")
    emit("message", {"msg": f"{username}: {message['msg']}"}, room=Room_Name)


@SocketIO.on('left', namespace='/sender')
def left(message):
    Room_Name: str = session.get("room_name")
    username: str = session.get("username")
    leave_room(room=Room_Name)
    session.clear
    emit("status", {"msg": f"{username}: has left the room :("}, room=Room_Name)

@SocketIO.on('file', namespace='/sender')
def handle_file(data):
    room = session.get('Room_Name')
    file_data = data['file'].split(",")[1]  # Extract base64 data
    file_name = data['fileName']
    file_bytes = base64.b64decode(file_data)
    file_stream = BytesIO(file_bytes)
    file_stream.seek(0)
    
    # Emit a message with a link to download the file
    file_url = url_for('download_temp_file', file_name=file_name, _external=True)
    emit('message', {
        'file': file_url,
        'fileName': file_name,
        'fileType': data['fileType'],
        'username': session.get('username')
    }, room=room)


# This is for the running 
if __name__ == '__main__':
    app.secret_key = "SECRET"
    app.run(debug=True, host=host, port=2024)
