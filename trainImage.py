import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image
from typing import Tuple, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_training_directory(path: str) -> None:
    """Validate the training directory exists and contains valid data."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Training directory not found: {path}")
    if not os.listdir(path):
        raise ValueError("Training directory is empty")

def process_image(image_path: str) -> Tuple[np.ndarray, int]:
    """Process a single image and extract face data and ID."""
    try:
        # Read and convert image to grayscale
        pilImage = Image.open(image_path).convert("L")
        imageNp = np.array(pilImage, "uint8")
        
        # Extract ID from filename (assuming format: Name_ID_number.jpg)
        Id = int(os.path.basename(image_path).split("_")[1])
        
        return imageNp, Id
    except Exception as e:
        logging.error(f"Error processing image {image_path}: {str(e)}")
        raise

def getImagesAndLables(path: str) -> Tuple[List[np.ndarray], List[int]]:
    """Get all training images and their corresponding IDs."""
    faces = []
    Ids = []
    
    # Validate directory
    validate_training_directory(path)
    
    # Process each person's directory
    for person_dir in os.listdir(path):
        person_path = os.path.join(path, person_dir)
        
        if not os.path.isdir(person_path):
            continue
            
        # Process each image in the person's directory
        for image_file in os.listdir(person_path):
            if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            image_path = os.path.join(person_path, image_file)
            try:
                face_data, person_id = process_image(image_path)
                faces.append(face_data)
                Ids.append(person_id)
            except Exception:
                continue  # Skip invalid images but continue processing others
                
    if not faces:
        raise ValueError("No valid training images found")
        
    return faces, Ids

def TrainImage(haarcasecade_path: str, trainimage_path: str, 
              trainimagelabel_path: str, message, text_to_speech) -> None:
    """Train the face recognition model with the provided images."""
    try:
        # Initialize face detector and recognizer
        detector = cv2.CascadeClassifier(haarcasecade_path)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Get training data
        faces, Ids = getImagesAndLables(trainimage_path)
        
        # Train the model
        recognizer.train(faces, np.array(Ids))
        
        # Save the trained model
        os.makedirs(os.path.dirname(trainimagelabel_path), exist_ok=True)
        recognizer.save(trainimagelabel_path)
        
        # Notify success
        success_msg = "Image Trained successfully"
        message.configure(text=success_msg)
        text_to_speech(success_msg)
        logging.info(success_msg)
        
    except Exception as e:
        error_msg = f"Error during training: {str(e)}"
        message.configure(text=error_msg)
        text_to_speech(error_msg)
        logging.error(error_msg)
        raise
