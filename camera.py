import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np
import pyrebase

class VideoCamera(object):
    def __init__(self, flip = False, file_type  = ".jpg", photo_string= "home/raspberry_user/pi/stream_photo"):
     
        self.vs = PiVideoStream().start()
        self.flip = flip 
        self.file_type = file_type 
        self.photo_string = photo_string 
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()

   
    def take_picture(self):
        config={
             "apiKey":"AIzaSyA-EpLwR5QMbg65iXo8iOVR5F9Fjf8LWB4",
             "authDomain":"test-74fe7.firebaseapp.com",
             "databaseURL":"https://test-74fe7-default-rtdb.firebaseio.com",
             "projectId":"test-74fe7",
             "storageBucket":"test-74fe7.appspot.com",
             "serviceAccount":"serviceAccountKey.json"}
 
 
 
        firebaseStorage = pyrebase.initialize_app(config)
        storage = firebaseStorage.storage()
        database = firebaseStorage.database()

        frame = self.flip_if_needed(self.vs.read())
        ret, image = cv.imencode(self.file_type, frame)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") 
        name=str(self.photo_string + "_" + today_date + self.file_type)
        cv.imwrite(name, frame)
        storage.child(name).put(name)
        uploaded_url=storage.child(name).get_url(None)
        image_metadata={
            "name":name,
            "url":uploaded_url}
        database.child("home/raspberry_user/pi").push(image_metadata)
