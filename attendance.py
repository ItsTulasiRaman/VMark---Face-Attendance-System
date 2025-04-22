import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Modern Color Scheme
COLORS = {
    'bg': '#ffffff',           # White background
    'primary': '#2196F3',      # Modern blue
    'secondary': '#757575',    # Gray
    'accent': '#FFC107',       # Amber
    'text': '#212121',         # Dark text
    'text_light': '#ffffff',   # White text
    'surface': '#f5f5f5',      # Light gray
    'error': '#f44336'         # Error red
}

# engine = pyttsx3.init()
# engine.say("Welcome!")
# engine.say("Please browse through your options..")
# engine.runAndWait()


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "./TrainingImageLabel/Trainner.yml"
)
trainimage_path = "/TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = (
    "./StudentDetails/studentdetails.csv"
)
attendance_path = "Attendance"

window = Tk()
window.title("VMark")
window.geometry("1280x720")
window.configure(background=COLORS['bg'])
window.resizable(False, False)


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Toplevel(window)
    sc1.geometry("400x110")
    try:
        sc1.iconbitmap("AMS.ico")
    except Exception:
        pass
    sc1.title("Warning!")
    sc1.configure(background=COLORS['bg'])
    sc1.resizable(0, 0)
    
    tk.Label(
        sc1,
        text="Enrollment & Name required!",
        fg=COLORS['error'],
        bg=COLORS['bg'],
        font=("Helvetica Neue", 16),
    ).pack(pady=10)
    
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg=COLORS['text_light'],
        bg=COLORS['primary'],
        width=10,
        height=1,
        relief='flat',
        cursor='hand2',
        font=("Helvetica Neue", 12),
    ).pack(pady=10)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


# Header Frame
header_frame = tk.Frame(window, bg=COLORS['bg'])
header_frame.pack(fill=X, pady=(20,0))

# Logo and Title Container
logo_title_frame = tk.Frame(header_frame, bg=COLORS['bg'])
logo_title_frame.pack()

# Logo
logo = Image.open("UI_Image/VMark_Logo.png")
logo = logo.resize((40, 40), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
l1 = tk.Label(logo_title_frame, image=logo1, bg=COLORS['bg'])
l1.pack(side=LEFT, padx=(0,10))

# Title
titl = tk.Label(
    logo_title_frame,
    text="VMark",
    bg=COLORS['bg'],
    fg=COLORS['primary'],
    font=("Helvetica Neue", 32, "bold"),
)
titl.pack(side=LEFT)

# Welcome Text
tk.Label(
    window,
    text="Welcome to VMark",
    bg=COLORS['bg'],
    fg=COLORS['text'],
    font=("Helvetica Neue", 36, "bold"),
).pack(pady=(40,60))

# Main Content Frame
content_frame = tk.Frame(window, bg=COLORS['bg'])
content_frame.pack(expand=True, fill=BOTH)

# Configure grid columns for even spacing
content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_columnconfigure(1, weight=1)
content_frame.grid_columnconfigure(2, weight=1)

def create_card(parent, image_path, button_text, command, column):
    # Card Frame
    card_frame = tk.Frame(parent, bg=COLORS['bg'])
    card_frame.grid(row=0, column=column, padx=20)
    
    # Image
    try:
        img = Image.open(image_path)
        img = img.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(card_frame, image=photo, bg=COLORS['bg'])
        img_label.image = photo
        img_label.pack(pady=(0,20))
    except Exception as e:
        print(f"Image not found: {e}")
    
    # Button
    btn = tk.Button(
        card_frame,
        text=button_text,
        command=command,
        font=("Helvetica Neue", 14),
        bg=COLORS['primary'],
        fg=COLORS['text_light'],
        relief='flat',
        cursor='hand2',
        width=20,
        pady=10
    )
    btn.pack()
    
    def on_enter(e):
        btn['background'] = '#1976D2'
    def on_leave(e):
        btn['background'] = COLORS['primary']
    
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    
    return card_frame

def TakeImageUI():
    ImageUI = Toplevel(window)
    ImageUI.title("Register Your Face")
    ImageUI.geometry("780x480")
    ImageUI.configure(background=COLORS['bg'])
    ImageUI.resizable(0, 0)
    
    # Header
    header_frame = tk.Frame(ImageUI, bg=COLORS['primary'], height=70)
    header_frame.pack(fill=X)
    
    tk.Label(
        header_frame,
        text="Register Your Face",
        bg=COLORS['primary'],
        fg=COLORS['text_light'],
        font=("Helvetica Neue", 24, "bold"),
    ).pack(pady=15)
    
    # Content Frame
    content_frame = tk.Frame(ImageUI, bg=COLORS['bg'])
    content_frame.pack(fill=BOTH, expand=True, padx=40, pady=20)
    
    # Form Fields
    def create_form_field(text, y_pos, validate_cmd=None):
        tk.Label(
            content_frame,
            text=text,
            bg=COLORS['bg'],
            fg=COLORS['text'],
            font=("Helvetica Neue", 14),
        ).place(x=120, y=y_pos)
        
        entry = tk.Entry(
            content_frame,
            font=("Helvetica Neue", 14),
            bg=COLORS['surface'],
            relief='flat',
            highlightthickness=1,
            highlightbackground="#e0e0e0",
            highlightcolor=COLORS['primary'],
            width=25,
        )
        entry.place(x=250, y=y_pos)
        
        if validate_cmd:
            entry.configure(validate="key", validatecommand=validate_cmd)
            
        return entry
    
    txt1 = create_form_field("Enrollment No:", 20, (ImageUI.register(testVal), "%P", "%d"))
    txt2 = create_form_field("Name:", 80)
    
    # Notification Area
    tk.Label(
        content_frame,
        text="Notification:",
        bg=COLORS['bg'],
        fg=COLORS['text'],
        font=("Helvetica Neue", 14),
    ).place(x=120, y=140)
    
    message = tk.Label(
        content_frame,
        text="",
        width=32,
        height=2,
        bg=COLORS['surface'],
        fg=COLORS['text'],
        font=("Helvetica Neue", 12),
    )
    message.place(x=250, y=140)
    
    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        if l1 and l2:
            takeImage.TakeImage(
                l1, l2, haarcasecade_path, trainimage_path,
                message, err_screen, text_to_speech
            )
            txt1.delete(0, "end")
            txt2.delete(0, "end")
        else:
            err_screen()
    
    # Buttons
    def create_action_button(text, command, x_pos):
        btn = tk.Button(
            content_frame,
            text=text,
            command=command,
            font=("Helvetica Neue", 14),
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            relief='flat',
            cursor='hand2',
            width=15,
            pady=10,
        )
        btn.place(x=x_pos, y=220)
        
        def on_enter(e):
            btn['background'] = '#1976D2'
        def on_leave(e):
            btn['background'] = COLORS['primary']
            
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
    create_action_button("Take Image", take_image, 130)
    create_action_button("Train Image", lambda: trainImage.TrainImage(
        haarcasecade_path, trainimage_path, trainimagelabel_path,
        message, text_to_speech), 360)

# Create cards
create_card(content_frame, "UI_Image/register.png", "Register a new student", TakeImageUI, 0)
create_card(content_frame, "UI_Image/attendance.png", "Take Attendance", 
           lambda: automaticAttedance.subjectChoose(text_to_speech), 1)
create_card(content_frame, "UI_Image/verifyy.png", "View Attendance", 
           lambda: show_attendance.subjectchoose(text_to_speech), 2)

# Exit Button Frame
exit_frame = tk.Frame(window, bg=COLORS['bg'])
exit_frame.pack(side=BOTTOM, pady=40)

# Exit Button
exit_btn = tk.Button(
    exit_frame,
    text="EXIT",
    command=window.quit,
    font=("Helvetica Neue", 14),
    bg=COLORS['primary'],
    fg=COLORS['text_light'],
    relief='flat',
    cursor='hand2',
    width=20,
    pady=10
)
exit_btn.pack()

def on_enter(e):
    exit_btn['background'] = '#1976D2'
def on_leave(e):
    exit_btn['background'] = COLORS['primary']

exit_btn.bind('<Enter>', on_enter)
exit_btn.bind('<Leave>', on_leave)

window.mainloop()
