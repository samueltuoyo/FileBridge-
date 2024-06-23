from flask import Flask, render_template, request, url_for, redirect, session, send_file
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = 'This is my Secret Key'
app.config["SESSION_TYPE"] = 'filesystem'

host = socket.gethostbyname(socket.gethostname())
Session(app)

DOWNLOAD = os.path.join(app.root_path, 'uploaded_files')
os.makedirs(DOWNLOAD, exist_ok=True)

SocketIO = SocketIO(app, manage_session=False)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/sender', methods=["GET", "POST"])
def sender():
    if request.method == "POST":
        username = request.form["username"]
        room_name = request.form["Room_Name"]
        if username == "0" and room_name == "0":
            return "<h1>Error 404</h1>"
        session["username"] = username
        session["Room_Name"] = room_name
        return render_template('share/sender.html', Session=session)
    else:
        if session.get('username') is not None:
            return render_template('share/receiver.html', Session=session)
        else:
            return redirect(url_for('receiver'))

@app.route('/receiver', methods=["GET", "POST"])
def receiver():
    return render_template('share/receiver.html')

@app.route('/download_temp/<file_name>')
def download_temp_file(file_name):
    file_data = request.args.get('file_data')
    file_bytes = base64.b64decode(file_data.split(",")[0])
    file_stream = BytesIO(file_bytes)
    file_stream.seek(0)
    return send_file(file_stream, as_attachment=True, download_name=file_name)

@app.route('/instructions')
def instructions():
    return render_template('instructions/instructions.html')

@app.route('/Downloads')
def to_downloads():
    return render_template('Downloads/Downloads.html')

@SocketIO.on('sender', namespace='/sender')
def sender(message):
    Room_Name = session.get('Room_Name')
    username = session.get('username')
    join_room(room=Room_Name)
    emit('status', {"msg": f"{username} has joined the room!!! "}, room=Room_Name)

@SocketIO.on("text", namespace="/sender")
def text(message):
    Room_Name = session.get("Room_Name")
    username = session.get("username")
    emit("message", {"msg": f"{username}: {message['msg']}"}, room=Room_Name)

@SocketIO.on('left', namespace='/sender')
def left(message):
    Room_Name = session.get("Room_Name")
    username = session.get("username")
    leave_room(room=Room_Name)
    session.clear()
    emit("status", {"msg": f"{username}: has left the room :("}, room=Room_Name)

@SocketIO.on('file', namespace='/sender')
def handle_file(data):
    room = session.get('Room_Name')
    file_data = data['file']
    file_name = data['fileName']
    emit('message', {'file': file_data, 'fileName': file_name, 'username': session.get('username')}, room=room)

if __name__ == '__main__':
    app.secret_key = "SECRET"
    app.run(debug=True, host=host, port=2024)
    # SocketIO.run()
