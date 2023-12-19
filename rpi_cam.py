
rpi = 0

# rpi 
if rpi:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    # end rpi
import time
import cv2
import face_recognition
import numpy as np
import os
import pandas as pd
import datetime
import time
import serial
from time import sleep
import os



#ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate

#received_data = ser.read()              #read serial port
                 
  

df = pd.read_csv('patient.csv')
df_delivered = df['name'].values.tolist()
df_names = df['name'].values.tolist()
source_folder = 'pre_images'
image_list = os.listdir(source_folder)

known_face_encodings = []
known_face_names = []

def get_time():
    now = datetime.datetime.now()
    return(str(now).split()[1].split(':')[0],str(now).split()[1].split(':')[1])

# start rpi
if rpi:
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # end rpi
else:
    video = cv2.VideoCapture(0)


time.sleep(0.1)
for img in image_list:

    image = face_recognition.load_image_file(os.getcwd()+'/'+source_folder+'/'+img)
    known_face_encodings.append(face_recognition.face_encodings(image)[0])
    known_face_names.append(img.split('.')[0])

# Initialize some variables

def back(*args):
    pass
cv2.namedWindow("Face Recognitation")

def recogonition(image):
    name = None
    face_locations = []
    face_encodings = []
    face_names = []
    image = cv2.resize(image,(320,240))
    
    small_frame = cv2.resize(image, (0, 0), fx=0.50, fy=0.50)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)
    
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
           
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2
            bottom +=5 
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(image, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, .5, (255, 255, 255), 1)
    return image,name
# rpi 
if rpi:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
        image = frame.array
        image = recogonition(image)
        cv2.imshow("Face Recognitation", image)
            
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break
else:
    while(1):
        ret,image = video.read()
        image,name = recogonition(image)
        cv2.imshow("Face Recognitation", image)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("u"):
            df = pd.read_csv('patient.csv')
        for d in df.values:
            h = int(str(d[1]).split(':')[0])
            m = int(str(d[1]).split(':')[1])
        #print(int(get_time()[0]))
        #print(1440-(int(get_time()[0])*60)+int(get_time()[1]),(1440-(h*60))+m)
            if name==d[0]:
                print(1440-(int(get_time()[0])*60)+int(get_time()[1]) ,(1440-(h*60))+m)
                t = abs((1440-(int(get_time()[0])*60)+int(get_time()[1])) - ((1440-(h*60))+m))
                print(t)
                if t>5:
                    
                    print(f"your tablets ready after {t} minuts")
                    
                if t<5:
                    if name not in df_delivered:
                        print("your tablets already delivered please collect")
                    else:
                        df_delivered.remove(name)
                        time.sleep(3)
                        print("your tablets ready to deliver")
                        os.system('echo "data" > /dev/ttyS0 ')
    ser.close()       
    video.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    
