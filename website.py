from flask import Flask, render_template, request, redirect, url_for, flash, Response
import os
from werkzeug.utils import secure_filename
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from mediapipe.framework.formats import landmark_pb2
from threading import Thread
from queue import Queue
import base64
import os
import math
from handframe import proccesFrame, compareGesture
import numpy
from handphoto import proccesFramePhoto
from flask import jsonify
from gesture import *
from flask_cors import CORS
import webbrowser



app = Flask(__name__)
name = "Jessalyn"
handMarks = '[]'
gestures = []
whereTo = ["https://www.youtube.com/watch?v=xvFZjo5PgG0&list=RDxvFZjo5PgG0&start_radio=1", ['https://wellesley-refresh.vercel.app']]

@app.route("/")
def hello_world(input = "Jess"):
    global name 
    name = input
    return render_template("hand.html", person=name, gestures = gestures, handMarks = "Upload First", whereTo=whereTo)

@app.route('/upload', methods=['POST'])
def upload():
    global gestures
    file = request.files['file']
    filebytes = file.read()
    npfile = numpy.frombuffer(filebytes, numpy.uint8)
    frame = cv2.imdecode(npfile, cv2.IMREAD_COLOR)
    proccesedFrame, landmarks = proccesFramePhoto(frame)
    gestures.append(landmarks)
    ret, jpeg = cv2.imencode(".jpg", proccesedFrame)
    jpegbytes = jpeg.tobytes()
    img = base64.b64encode(jpegbytes).decode('utf-8')
    
    return render_template("hand.html", person=name, gestures = gestures, result_url = img, handmarksphoto=str(landmarks), whereTo=whereTo)

@app.route('/drop_down', methods=['GET', 'POST'])
def dropdown():
    
    return render_template("hand.html", person = name, message = "NEW CLICK", gestures = gestures, whereTo=whereTo )

def generateFrame():
    global handMarks
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()

     
        proccessedFrame, handMarks = proccesFrame(frame)
       

        ret, jpeg = cv2.imencode(".jpg", proccessedFrame)
        jpegbytes = jpeg.tobytes()

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpegbytes + b'\r\n')

@app.route('/getLandMarks')
def getLandMarks():
    global handMarks
    return jsonify({'landmarks': handMarks})

@app.route('/checkGesture')
def checkGesture():
    global gestures
    if len(gestures) == 0:
        return jsonify({'result': False, 'id': 0}) 
    for gestureID, gesture in enumerate(gestures):
        result = compareGesture(handMarks, gesture)
        if result:
            return jsonify({'result': result, 'id': gestureID}) 
    return jsonify({'result': False, 'id': 'N/A'}) 

@app.route('/video_feed')
def video_feed():
    return Response(generateFrame(), mimetype='multipart/x-mixed-replace; boundary=frame')

