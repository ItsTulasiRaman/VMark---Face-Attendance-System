import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import Image
import shutil

def validate_inputs(l1, l2):
    """Validate enrollment number and name inputs."""
    if not l1 and not l2:
        return False, 'Please Enter your Enrollment Number and Name.'
    elif not l1:
        return False, 'Please Enter your Enrollment Number.'
    elif not l2:
        return False, 'Please Enter your Name.'
    return True, None

def create_student_directory(path):
    """Create or clean student directory."""
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def setup_camera():
    """Initialize and validate camera."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Could not open camera")
    return cam

def capture_face_samples(cam, detector, path, name, enrollment):
    """Capture face samples and save them."""
    sampleNum = 0
    cv2.namedWindow("Face Capture", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Face Capture", 640, 480)
    
    while True:
        ret, img = cam.read()
        if not ret:
            raise Exception("Failed to grab frame")
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            sampleNum += 1
            cv2.imwrite(
                os.path.join(path, f"{name}_{enrollment}_{sampleNum}.jpg"),
                gray[y:y + h, x:x + w],
            )
        
        cv2.imshow("Face Capture", img)
        
        if cv2.waitKey(1) & 0xFF == ord("q") or sampleNum > 50:
            break
            
    return sampleNum

def save_student_details(enrollment, name, csv_path):
    """Save student details to CSV file."""
    row = [enrollment, name]
    with open(csv_path, "a+", newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=",")
        writer.writerow(row)

def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    """Main function to capture student images and save details."""
    # Validate inputs
    is_valid, error_msg = validate_inputs(l1, l2)
    if not is_valid:
        text_to_speech(error_msg)
        err_screen()
        return
        
    cam = None
    try:
        # Setup camera and detector
        cam = setup_camera()
        detector = cv2.CascadeClassifier(haarcasecade_path)
        
        # Create student directory
        directory = f"{l1}_{l2}"
        path = os.path.join(trainimage_path, directory)
        create_student_directory(path)
        
        # Capture face samples
        sampleNum = capture_face_samples(cam, detector, path, l2, l1)
        
        # Clean up camera
        if cam is not None:
            cam.release()
        cv2.destroyAllWindows()
        
        # Process results
        if sampleNum > 0:
            save_student_details(l1, l2, "StudentDetails/studentdetails.csv")
            res = f"Images Saved for ER No: {l1} Name: {l2}"
            message.configure(text=res)
            text_to_speech(res)
        else:
            raise Exception("No faces detected during capture")
            
    except Exception as e:
        error_msg = str(e)
        text_to_speech(error_msg)
        message.configure(text=error_msg)
        if cam is not None:
            cam.release()
        cv2.destroyAllWindows()

def getImagesAndLables(path):
    imagePaths = []
    faceSamples = []
    ids = []
    
    try:
        # Get all files in directory
        for filename in os.listdir(path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                imagePaths.append(os.path.join(path, filename))

        for imagePath in imagePaths:
            # Load the image and convert it to grayscale
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')

            # Get the ID from the image file name
            id = int(os.path.split(imagePath)[-1].split(".")[0])
            
            faceSamples.append(img_numpy)
            ids.append(id)
            
    except Exception as e:
        print(f"Error in getImagesAndLables: {str(e)}")
        raise
        
    return faceSamples, ids

def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    try:
        print(f"Training with images from: {trainimage_path}")
        
        # Ensure directory exists
        if not os.path.exists(trainimage_path):
            os.makedirs(trainimage_path)
            message.configure(text="No training images found")
            text_to_speech("No training images found")
            return

        # Get faces and IDs
        faces, Ids = getImagesAndLables(trainimage_path)
        
        if len(faces) == 0:
            message.configure(text="No faces found in training images")
            text_to_speech("No faces found in training images")
            return

        # Create and train the recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, np.array(Ids))

        # Ensure the directory for the trainer file exists
        trainer_dir = os.path.dirname(trainimagelabel_path)
        if not os.path.exists(trainer_dir):
            os.makedirs(trainer_dir)

        # Save the trained model
        recognizer.write(trainimagelabel_path)
        
        message.configure(text="Model Trained Successfully")
        text_to_speech("Model Trained Successfully")

    except Exception as e:
        print(f"Error training images: {str(e)}")
        message.configure(text=f"Error training images: {str(e)}")
        text_to_speech("Error occurred while training images")
