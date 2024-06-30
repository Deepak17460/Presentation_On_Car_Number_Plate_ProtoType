import os
import psycopg2
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import anpr
import odalpr
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import db

load_dotenv()

# Creating the flask app
app = Flask(__name__)
socketio = SocketIO(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})  # Allow requests from http://localhost:4200
url = os.getenv("DATABASE_URL")
#url="postgresql://postgres:Bhardwaj#123@localhost/dpcode"
# api = Api(app)
progress = -1

# Establishing a database connection
connection = psycopg2.connect(url) # -> this is a function
try:
    with connection.cursor() as cursor:  # -> this is a method
        db.create_table(cursor=cursor)
    connection.commit() # -> Transanction for database inconsistency & integrity
except:
    pass


@app.route('/get_data',methods=['GET'])
def get_data():
    try:
        res = None
        with connection.cursor() as cursor:
            cursor.execute("select * from Vehicle_Record order by id desc;")
            res = cursor.fetchall()
        
        return jsonify(res),200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/video',methods=['POST'])
def upload_video():
    try:
        
        video_file = request.files['video']
        
        print(video_file)
        video_file.save('video.mp4')

        t = Thread(target=anpr.ImageProcessing, args=['./video.mp4',socketio,connection])
        t.run()
        # result=anpr.ImageProcessing('video.mp4')
        print("Completed")
        return jsonify({ message: "Processing" }),200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/optimal',methods=['POST'])
def Action_video():
    try:
        
        video_file = request.files['video']
        print(video_file)
        video_file.save('video.mp4')
        t= Thread(target=odalpr.Optimal, args=['./video.mp4',socketio,connection])
        t.run()


        print("Completed")
        return  jsonify({ message: "Processing" }),200

    except Exception as e:
        return jsonify({"error": str(e)}),500

    
# sockets
@socketio.on("connect")
def connect():
    print("A client connected!")

@socketio.on("disconnect")
def disconnect():
    print("A client disconnected!")

@socketio.on("progress")
def message(message):
    print("Received message: {}".format(message))
    socketio.emit("message", message, broadcast=True)


if __name__ == '__main__':
    app.run(debug=True)
