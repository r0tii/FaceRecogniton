import cv2
import os
import numpy as np
from baza import Database

class FaceRecognizer(object):
    def __init__(self, xml_path, index=0,):
        self.camera = cv2.VideoCapture(index)
        self.index = index
        self.haar_cascade = cv2.CascadeClassifier(xml_path)
        self.xml_path = xml_path
        self.recognizer = cv2.face.createLBPHFaceRecognizer()
        self.db1 = Database("Face_Recognition\\Database\\baza.db")

    def __del__(self):
        self.camera.release()
        print("Program finished, memory de-allocated, camera closed") 

    def normalize(self, roi):
        width, height = 200, 200
        gray = cv2.equalizeHist(roi) #Equalizes the histogram of a grayscale image - better contrast
        resized_img = cv2.resize(gray, (height, width))
        return resized_img

    def detect_store(self, first, path):
        counter = 0
        input("I will take 20 pictures, press ENTER when you ready")
        while(self.camera.isOpened() and counter < 100):
            ret, frame = self.camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_rects = self.haar_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.3,
            minNeighbors=5,
            minSize=(30, 30)
            )
            for (x,y,w,h) in face_rects:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                gray_roi = gray[y:y+h, x:x+w]
                cv2.putText(frame,"Face Detected",(10,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
                print(counter)
                if(counter > 70 and counter < 101): #to give user some time to prepare
                    cv2.imwrite(path + "\\" + first + "." + str(counter-70) + ".jpg", self.normalize(gray_roi))
                    print("saving {}. frame".format(counter))
                    #cv2.imshow("Saving..", self.normalize(gray_roi))
            counter += 1
            cv2.imshow("ESC to close", frame)
            key = cv2.waitKey(1)
            if(key == 27):
                break
        cv2.destroyAllWindows()

    def get_images_and_labels(self, path):
        images = []
        labels = []
        counter = None
        for person in os.listdir(path):
            first, last = (person.split("_"))
            counter = self.db1.get_id(first, last)[0]
            for image in os.listdir(os.path.join(path, person)): #if(image.endswith(".jpg")):
                try:
                    print(os.path.join(path, person, image))
                    img = cv2.imread(os.path.join(path, person, image), cv2.IMREAD_GRAYSCALE)
                    np_image = np.array(img, "uint8")
                    images.append(np_image)
                    labels.append(counter)
                    print(counter)
                    cv2.imshow("training", np_image)
                    cv2.waitKey(10)
                except OSError as e:
                        print(e)
        cv2.destroyAllWindows()
        return images, np.array(labels)

    def train_recognizer(self):
        path = "Face_Recognition\\People\\"
        model_path = "Face_Recognition\\Recognizer\\data.xml"
        images, labels = self.get_images_and_labels(path)
        self.recognizer.train(images, labels)
        self.recognizer.save(model_path)
        return model_path

    def recognize(self):
        model_path = self.train_recognizer()
        self.recognizer.load(model_path)
        while(self.camera.isOpened()):
            ret, frame = self.camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_rects = self.haar_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.3,
            minNeighbors=5,
            minSize=(30, 30)
            )
            for (x,y,w,h) in face_rects:
                gray_roi = gray[y:y+h, x:x+w]
                collector = cv2.face.MinDistancePredictCollector()
                self.recognizer.predict(gray_roi, collector)
                conf = collector.getDist()
                pred = collector.getLabel()
                treshold = 70 #you need to play with it
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                if(conf < treshold):
                    profile = self.db1.get_name(str(pred))
                    cv2.putText(frame,str(profile[0]),(x,y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
                    cv2.putText(frame,str(profile[1]),(x,y+h+60), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
                    print("Current face XY location is {}".format(x,y))
                else:
                    cv2.putText(frame,"Unknown",(x,y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
                    
            cv2.imshow("Face Recognizer", frame)
            key = cv2.waitKey(1)
            if(key == 27):
                break
        cv2.destroyAllWindows()