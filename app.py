from flask import Flask, render_template, url_for  

app = Flask(__name__)
# These are the routes for the url and radiation page 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/sender')
def sender():
    return render_template('share/sender.html')

@app.route('/receiver')
def receiver():
    return render_template('share/receiver.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions/instructions.html')

@app.route('/mp3')
def to_mp3():
    return render_template('To-mp3/video-to-mp3.html')

# This is for the running 
if __name__ == '__main__':
    app.run(debug=True)