import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os, cv2, shutil, csv, datetime, time
import numpy as np
from PIL import ImageTk, Image, ImageDraw
import pandas as pd
import pyttsx3
import sys

# Import project modules
import show_attendance
import takeImage
import trainImage
import automaticAttedance

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# Paths settings
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)
studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# Add after the path definitions
required_dirs = [
    "./TrainingImageLabel",
    "./TrainingImage",
    "./StudentDetails",
    "Attendance"
]

for dir_path in required_dirs:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# Functions for popup errors
def del_sc1():
    global sc1
    sc1.destroy()

def err_screen():
    global sc1
    sc1 = tk.Toplevel(window)
    sc1.geometry("400x110")
    try:
        sc1.iconbitmap("AMS.ico")
    except Exception:
        pass
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    lbl = ttk.Label(sc1, text="Enrollment & Name required!!!", foreground="yellow", background="#1c1c1c",
                     font=("Verdana", 16, "bold"))
    lbl.pack(pady=10)
    btn = ttk.Button(sc1, text="OK", command=del_sc1)
    btn.pack(pady=5)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

# Main Window Setup
window = tk.Tk()
window.title("VMark")
window.geometry("1280x720")
window.configure(background="#f0f0f0")
window.resizable(False, False)

# Header Frame with Logo and Title
header_frame = tk.Frame(window, bg="#ffffff")
header_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

# Load and place the logo image
try:
    logo_image = Image.open("UI_Image/VMark_Logo.png")
    logo_image = logo_image.resize((90, 47), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(header_frame, image=logo_photo, bg="#ffffff")
    logo_label.image = logo_photo
    logo_label.pack(side=tk.LEFT, padx=20)
except Exception as e:
    print("Logo not found:", e)

title_label = tk.Label(header_frame, 
                      text="Smart way to check in!", 
                      bg="#ffffff", 
                      fg="#333333",
                      font=("Helvetica Neue", 30, "bold"))
title_label.pack(side=tk.LEFT)

# Main Content Frame
main_frame = tk.Frame(window, bg="#f0f0f0")
main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

# Configure grid columns
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

def create_custom_button(parent, text, command, width=20):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Helvetica Neue", 14),
        fg="white",
        bg="#0095ff",
        cursor="hand2",
        padx=20,
        pady=10,
        width=width,
        relief="flat",
        activebackground="#0077cc",
        activeforeground="white"
    )
    
    def on_enter(e):
        button.configure(bg="#0077cc")
        
    def on_leave(e):
        button.configure(bg="#0095ff")
    
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)
    
    return button

def TakeImageUI():
    ImageUI = tk.Toplevel(window)
    ImageUI.title("Register Your Face")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#ffffff")
    ImageUI.resizable(False, False)
    
    # Header in Toplevel with gradient effect
    header_frame = tk.Frame(ImageUI, bg="#0095ff", height=70)
    header_frame.pack(fill=tk.X)
    header_label = tk.Label(
        header_frame, 
        text="Register Your Face",
        fg="white",
        bg="#0095ff",
        font=("Helvetica Neue", 24, "bold")
    )
    header_label.pack(pady=15)
    
    # Main content frame
    content_frame = tk.Frame(ImageUI, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
    
    # Form Frame with modern styling
    form_frame = tk.Frame(content_frame, bg="white")
    form_frame.pack(fill=tk.X, pady=20)
    
    def create_entry_with_label(parent, label_text, row, validate_cmd=None):
        # Label
        label = tk.Label(
            parent,
            text=label_text,
            font=("Helvetica Neue", 12),
            fg="#333333",
            bg="white"
        )
        label.grid(row=row, column=0, padx=(0, 20), pady=10, sticky="e")
        
        # Entry with modern styling
        entry = tk.Entry(
            parent,
            font=("Helvetica Neue", 12),
            bg="#f0f0f0",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#e0e0e0",
            highlightcolor="#0095ff",
            width=30
        )
        entry.grid(row=row, column=1, pady=10, sticky="ew")
        
        if validate_cmd:
            entry.config(validate="key", validatecommand=validate_cmd)
        
        return entry
    
    # Create form fields
    en_entry = create_entry_with_label(
        form_frame, 
        "Enrollment No:", 
        0, 
        (form_frame.register(testVal), "%P", "%d")
    )
    
    name_entry = create_entry_with_label(
        form_frame, 
        "Name:", 
        1
    )
    
    # Notification area with modern styling
    notif_frame = tk.Frame(content_frame, bg="white")
    notif_frame.pack(fill=tk.X, pady=20)
    
    notif_label = tk.Label(
        notif_frame,
        text="Notification:",
        font=("Helvetica Neue", 12),
        fg="#333333",
        bg="white"
    )
    notif_label.pack(side=tk.LEFT, padx=(95, 10))
    
    notif_msg = tk.Label(
        notif_frame,
        text="",
        font=("Helvetica Neue", 12),
        fg="#666666",
        bg="#f8f8f8",
        width=30,
        height=2
    )
    notif_msg.pack(side=tk.LEFT)
    
    # Button Frame with modern styling
    btn_frame = tk.Frame(content_frame, bg="white")
    btn_frame.pack(pady=30)
    
    def create_custom_button(parent, text, command, primary=True):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Helvetica Neue", 12),
            fg="white",
            bg="#0095ff" if primary else "#666666",
            activebackground="#0077cc" if primary else "#555555",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=15,
        height=2,
            bd=0
        )
        
        def on_enter(e):
            btn['background'] = '#0077cc' if primary else '#555555'
            
        def on_leave(e):
            btn['background'] = '#0095ff' if primary else '#666666'
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn

    def take_image():
        en = en_entry.get()
        nm = name_entry.get()
        if en and nm:  # Add validation
            takeImage.TakeImage(
                en, nm, haarcasecade_path, trainimage_path, 
                notif_msg, err_screen, text_to_speech
            )
            en_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
        else:
            err_screen()

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path, trainimage_path,
            trainimagelabel_path, notif_msg, text_to_speech
        )
    
    # Create buttons with modern styling
    take_img_btn = create_custom_button(btn_frame, "Take Image", take_image, True)
    take_img_btn.pack(side=tk.LEFT, padx=10)
    
    train_img_btn = create_custom_button(btn_frame, "Train Image", train_image, False)
    train_img_btn.pack(side=tk.LEFT, padx=10)

    # Configure grid weights
    form_frame.grid_columnconfigure(1, weight=1)

# Update the card data to use TakeImageUI directly
card_data = [
    ("UI_Image/register.png", "Register a New Student", TakeImageUI),
    ("UI_Image/attendance.png", "Take Attendance", 
     lambda: automaticAttedance.subjectChoose(text_to_speech)),
    ("UI_Image/verifyy.png", "View Attendance", 
     lambda: show_attendance.subjectchoose(text_to_speech))
]

for i, (image_path, button_text, command) in enumerate(card_data):
    # Create card frame
    card = tk.Frame(main_frame, bg="white", highlightthickness=1, 
                   highlightbackground="#e0e0e0")
    card.grid(row=0, column=i, padx=20, pady=20, sticky="nsew")
    
    # Configure card layout
    card.grid_rowconfigure(1, weight=1)
    
    # Load and display image
    try:
        img = Image.open(image_path)
        img = img.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(card, image=photo, bg="white")
        img_label.image = photo
        img_label.pack(pady=(40, 0))
    except Exception as e:
        print(f"Image not found: {e}")
    
    # Add spacer frame to push button to bottom
    spacer = tk.Frame(card, bg="white")
    spacer.pack(expand=True, fill="both")
    
    # Create and pack button
    button = create_custom_button(card, button_text, command)
    button.pack(pady=(0, 20))

# Footer frame
footer_frame = tk.Frame(window, bg="#f0f0f0")
footer_frame.pack(side=tk.BOTTOM, pady=20)

# Exit button
exit_button = create_custom_button(footer_frame, "EXIT", window.quit, width=10)
exit_button.pack()

# Add this after window creation to enable rounded corners on Windows
def enable_rounded_corners():
    try:
        from ctypes import windll, byref, sizeof, c_int
        windll.dwmapi.DwmSetWindowAttribute(
            windll.user32.GetParent(window.winfo_id()),
            35,  # DWMWA_WINDOW_CORNER_PREFERENCE
            byref(c_int(2)),  # DWMWCP_ROUND
            sizeof(c_int)
        )
    except:
        pass

window.after(10, enable_rounded_corners)

# Start the main loop
window.mainloop()
