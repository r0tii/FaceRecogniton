import os
import sys
from baza import Database
from faceRecognizer import FaceRecognizer

def create_dirs(path):
    r_paths = ["People", "Database", "Recognizer"]
    counter = 0
    while counter <1:
        for folder in r_paths:
            x = os.path.join(path.split("\\")[0], folder)
            if not os.path.exists(x):
                os.makedirs(x)
        counter+=1
    if not os.path.exists(path):
            os.makedirs(path)
 
def user_input():
    print (30 * "-")
    print ("       POSSIBLE ACTIONS")
    print (30 * "-")
    print ("1. JUST DO IT!!!!")
    print ("2. Add person to the database / Face Detection")
    print ("3. Test the face recognizer / Face Recognition (use only after 1. or 2. choice)")
    print ("4. Exit")
    print (30 * "-")
    
    while True:
        try:
            choice = int(input(">>>Enter your choice [1-5]: "))
        except ValueError:
            print("Error! Input needs to be integer only")
            continue
        if(choice not in range(1, 6)):
            print("Error! Please enter a number between [1-5]")
            continue
        else:
            return choice 

def main():
    CHOICE = user_input()

    if(CHOICE == 1):
        first, last = input(">>>Please enter your full name: ").split()
        path = "Face_Recognition\\People\\" + first.capitalize() + "_" + last.capitalize()
        create_dirs(path)
        db1 = Database("Face_Recognition\\Database\\baza.db")
        rec1 = FaceRecognizer("haarcascade_frontalface_default.xml")
        db1.insert_data(first.capitalize(), last.capitalize(), path)
        rec1.detect_store(first, path)
        rec1.recognize()
    elif(CHOICE == 2):
        first, last = input(">>>Please enter your full name: ").split()
        path = "Face_Recognition\\People\\" + first.capitalize() + "_" + last.capitalize()
        create_dirs(path)
        db1 = Database("Face_Recognition\\Database\\baza.db")
        rec1 = FaceRecognizer("haarcascade_frontalface_default.xml")
        db1.insert_data(first.capitalize(), last.capitalize(), path)
        rec1.detect_store(first, path)
    elif(CHOICE == 3):
        try:
            rec1 = FaceRecognizer("haarcascade_frontalface_default.xml")
            rec1.recognize()
        except Exception as e:
            print("Use 1. or 2. choice first! Error:{}".format(e))
    elif(CHOICE == 4):
        sys.exit()
  
if __name__ == "__main__":        
    main()