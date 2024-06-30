import cv2
import numpy as np
import imutils
import easyocr
from datetime import datetime, timedelta
import db
from time import gmtime, strftime
import re
# from cv2 import dnn_superres
INSERT_VEHICLE = "INSERT INTO Vehicle_Record (carNo, inTime) VALUES (%s, %s);"


sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel("dnn_model/EDSR_x4.pb")
sr.setModel('edsr', 4)
reader = easyocr.Reader(['en'])
# sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CANN)
# sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# load video
def ImageProcessing(video,socket,connection):
   # print("dpcodeXyJkWKdWXO80bdK7tzDbO2pUSpXmyQAz0/RGroSpBs+ACRCVuIhv")
    cap = cv2.VideoCapture(video)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    result_array = []



    # read frames
    ret = True
    count = 1
    while ret:
        ret, frame = cap.read()
        # print(frame)
        # print(frame.shape)
       # print(count*100/length)
        count = count + 1
    
        if ret:
            try:
                (h, w) = frame.shape[:2]
                # img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                frame = frame[600:800, 500:]
            
                (cX, cY) = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D((cX, cY), -25, 1.0)
                frame = cv2.warpAffine(frame, M, (w, h))

                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # convert to grey scale
                # gray = gray[600:800, 500:]
                bfilter = cv2.bilateralFilter(gray, 11, 17, 17) # --> Noise reduction
                edged = cv2.Canny(bfilter, 30, 200) # --> Edge detection

                keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = imutils.grab_contours(keypoints)
                contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
                location = None
                for contour in contours:
                    approx = cv2.approxPolyDP(contour, 10, True)
                    if len(approx) == 4:
                        location = approx
                        break

                mask = np.zeros(gray.shape, np.uint8)
                new_image = cv2.drawContours(mask, [location], 0,255, -1)
                # new_image = cv2.bitwise_and(frame, frame, mask=mask)

                (x,y) = np.where(mask==255)
                (x1, y1) = (np.min(x), np.min(y))
                (x2, y2) = (np.max(x), np.max(y))
                cropped_image = frame[x1:x2+20, y1:y2+20]
                upscalled = sr.upsample(cropped_image)

               
                result = reader.readtext(upscalled)
                socket.emit("progress", (count*100/length))
                print(result)
                if len(result) != 0:

                    result_array.append({'carNo':result[0][1],'timestamp':datetime.now()})
                    plate = re.sub('[^A-Za-z0-9]+', '',result[0][1]).upper()

                    res = []

                    cursor = connection.cursor() 
                    cursor.execute("select * from Vehicle_Record where carNo = %s and inTime > %s ;",(plate, (datetime.now() +timedelta(hours=5, minutes=30) - timedelta(hours=0, minutes=1)).strftime("%Y-%m-%d %H:%M:%S")))
                    res = cursor.fetchall()
                    connection.commit()

                    #print(INSERT_VEHICLE, (plate, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                    if(len(res) == 0):
                        cursor = connection.cursor()
                        cursor.execute(INSERT_VEHICLE, (plate, (datetime.now()+timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")))
                        connection.commit()

            except Exception as e:
                print(e)
                pass

    return result_array
