import cv2
import numpy as np
import datetime
from object_detection import ObjectDetection
import requests
import datetime
from pprint import pprint
import db
import re
from datetime import datetime, timedelta

INSERT_VEHICLE = "INSERT INTO Vehicle_Record (carNo, inTime) VALUES (%s, %s);"
od = ObjectDetection()

def check_frame(fp) -> dict:
    success, image_jpg = cv2.imencode('.jpg', fp)
    regions = ["in"]
    response = requests.post('https://api.platerecognizer.com/v1/plate-reader/',
                             data=dict(regions=regions),
                             files=dict(upload=image_jpg.tostring()),
                             headers={'Authorization': 'Token ff12b10667cb1048b171036994092f6ac128d4bf'})
    data = response.json()
    res = {}

    try:
        res['plate'] = data["results"][0]["candidates"][0]['plate']
        res['type'] = data["results"][0]["vehicle"][0]['type']
    except:
        pass
    return res
def Optimal(location,socket,connection):
    cap = cv2.VideoCapture(location)
    result_array = []
    frame_window = [0]
    ret = True
    detected = False
    count = 1
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while ret: # it is true
        ret, frame = cap.read()

        if ret: # true
            img = frame
            frame = frame[400:] # crop out a portion of the video frame that is not needed for object detection

            (class_ids, scores, boxes) = od.detect(frame)
            print(class_ids)

            if len(class_ids) > 0:
                if not detected:
                    i = 24
                    while i != 0 and len(frame_window) > 0:
                        if frame_window[-1] == 0:
                            frame_window.pop()
                        i = i - 1

                    if len(frame_window) > 0 and frame_window[-1] == 0:
                       # cv2.imwrite(strftime("./images/%Y-%m-%d-%M-%S", gmtime()) + ".jpg", img)
                        temp = check_frame(img)
                        print(temp)
                        if 'plate' in temp:
                            result_array.append({"carNo":temp['plate'],'timestamp':datetime.now().isoformat()})
                           
                            plate = re.sub('[^A-Za-z0-9]+', '',temp['plate']).upper() # Converting in Uppser-Case
                            res = []
                            cursor = connection.cursor() 
                            cursor.execute("select * from Vehicle_Record where carNo = %s and inTime > %s ;",(plate, (datetime.now() +timedelta(hours=5, minutes=30) - timedelta(hours=0, minutes=5)).strftime("%Y-%m-%d %H:%M:%S")))
                            res = cursor.fetchall()
                            connection.commit()
                            if(len(res) == 0):
                                cursor = connection.cursor()
                                cursor.execute(INSERT_VEHICLE, (plate, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                connection.commit()
                    else:
                        if len(frame_window) == 0:
                            frame_window.append(1)
                           # cv2.imwrite(strftime("./images/%Y-%m-%d-%M-%S", gmtime()) + ".jpg", img)
                            temp = check_frame(img)
                            print(temp)
                            if 'plate' in temp:
                                result_array.append({"carNo":temp['plate'],'timestamp':datetime.now().isoformat()})

                                plate = re.sub('[^A-Za-z0-9]+', '',temp['plate']).upper()
                                res = []
                                cursor = connection.cursor() 
                                cursor.execute("select * from Vehicle_Record where carNo = %s and inTime > %s ;",(plate, (datetime.now() +timedelta(hours=5, minutes=30) - timedelta(hours=0, minutes=5)).strftime("%Y-%m-%d %H:%M:%S")))
                                res = cursor.fetchall()
                                connection.commit()
                                if(len(res) == 0):
                                    cursor = connection.cursor()
                                    cursor.execute(INSERT_VEHICLE, (plate, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                    connection.commit()

                detected = True
            else:
                detected = False
                frame_window.append(0)

            print(count)
            count = count + 1

            if len(frame_window) > 25:
                frame_window.pop(0)
            socket.emit("progress", (count*100/length))

    return result_array
