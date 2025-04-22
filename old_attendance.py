"""
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
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="#1c1c1c")  # Dark theme


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",  # Dark background for the error window
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",  # Darker button color
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


logo = Image.open("UI_Image/VMark_Logo.png")
logo = logo.resize((90, 47), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
titl = tk.Label(window, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1, bg="#1c1c1c",)
l1.place(x=630, y=10)

titl = tk.Label(
    window, text="VMark", bg="#1c1c1c", fg="yellow", font=("Verdana", 27, "bold"),
)
titl.place(x=725, y=12)

a = tk.Label(
    window,
    text="Welcome to VMark",
    bg="#1c1c1c",  # Dark background for the main text
    fg="yellow",  # Bright yellow text color
    bd=10,
    font=("Verdana", 35, "bold"),
)
a.pack()

ri = Image.open("UI_Image/register.png")
r = ImageTk.PhotoImage(ri)
label1 = Label(window, image=r)
label1.image = r
label1.place(x=100, y=270)

ai = Image.open("UI_Image/attendance.png")
a = ImageTk.PhotoImage(ai)
label2 = Label(window, image=a)
label2.image = a
label2.place(x=980, y=270)

vi = Image.open("UI_Image/verifyy.png")
v = ImageTk.PhotoImage(vi)
label3 = Label(window, image=v)
label3.image = v
label3.place(x=600, y=270)


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")  # Dark background for the image window
    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)
    # image and title
    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="#1c1c1c", fg="green", font=("Verdana", 30, "bold"),
    )
    titl.place(x=270, y=12)

    # heading
    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#1c1c1c",  # Dark background for the details label
        fg="yellow",  # Bright yellow text color
        bd=10,
        font=("Verdana", 24, "bold"),
    )
    a.place(x=280, y=75)

    # ER no
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="#333333",  # Dark input background
        fg="yellow",  # Bright text color for input
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#333333",  # Dark input background
        fg="yellow",  # Bright text color for input
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="#333333",  # Dark background for messages
        fg="yellow",  # Bright text color for messages
        relief=RIDGE,
        font=("Verdana", 14, "bold"),
    )
    message.place(x=250, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",  # Dark background for the button
        fg="yellow",  # Bright text color for the button
        height=2,
        width=12,
        relief=RIDGE,
    )
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # train Image function call
    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",  # Dark background for the button
        fg="yellow",  # Bright text color for the button
        height=2,
        width=12,
        relief=RIDGE,
    )
    trainImg.place(x=360, y=350)


r = tk.Button(
    window,
    text="Register a new student",
    command=TakeImageUI,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=100, y=520)


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


r = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attedance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=600, y=520)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


r = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=1000, y=520)
r = tk.Button(
    window,
    text="EXIT",
    bd=10,
    command=quit,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=600, y=660)


window.mainloop()
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os, cv2, shutil, csv, datetime, time
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import pyttsx3

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
window.configure(background="#e6e6e6")
window.resizable(False, False)

# Setup ttk Style with a dark theme
style = ttk.Style(window)
style.theme_use("clam")
style.configure("TFrame", background="#e6e6e6")
style.configure("TLabel", background="#e6e6e6", foreground="yellow", font=("Verdana", 14))
style.configure("Header.TLabel", font=("Helvetica Neue", 30, "bold"), foreground="#1c1c1c", background="#e6e6e6")
style.configure("TButton", font=("Helvetica Neue", 16, "bold"), foreground="yellow", background="#333333", padding=10)
style.map("TButton",
          background=[('active', '#555555')],
          foreground=[('active', 'yellow')])

# Header Frame with Logo and Title
header_frame = ttk.Frame(window)
header_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

# Load and place the logo image
try:
    logo_image = Image.open("UI_Image/VMark_Logo.png")
    logo_image = logo_image.resize((90, 47), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ttk.Label(header_frame, image=logo_photo)
    logo_label.image = logo_photo
    logo_label.pack(side=tk.LEFT, padx=20)
except Exception as e:
    print("Logo not found:", e)

title_label = ttk.Label(header_frame, text="Smart way to check in!", style="Header.TLabel")
title_label.pack(side=tk.LEFT)

# Main Content Frame (Centering the three cards)
main_frame = ttk.Frame(window)
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Configure grid columns equally so cards are centered
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)

# -------------------------------------------------------------------
# Card 1: Register a new student
card1 = ttk.Frame(main_frame, relief="ridge", borderwidth=2)
card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
# Load register image
try:
    reg_image = Image.open("UI_Image/register.png")
    reg_image = reg_image.resize((200, 200), Image.LANCZOS)
    reg_photo = ImageTk.PhotoImage(reg_image)
    reg_label = ttk.Label(card1, image=reg_photo)
    reg_label.image = reg_photo
    reg_label.pack(pady=(20,10))
except Exception as e:
    print("Register image not found:", e)
reg_button = ttk.Button(card1, text="Register a New Student", command=lambda: TakeImageUI())
reg_button.pack(pady=(0,20))

# -------------------------------------------------------------------
# Card 2: Take Attendance
card2 = ttk.Frame(main_frame, relief="ridge", borderwidth=2)
card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
# Load attendance image
try:
    attend_image = Image.open("UI_Image/attendance.png")
    attend_image = attend_image.resize((200, 200), Image.LANCZOS)
    attend_photo = ImageTk.PhotoImage(attend_image)
    attend_label = ttk.Label(card2, image=attend_photo)
    attend_label.image = attend_photo
    attend_label.pack(pady=(20,10))
except Exception as e:
    print("Attendance image not found:", e)
attend_button = ttk.Button(card2, text="Take Attendance", command=lambda: automaticAttedance.subjectChoose(text_to_speech))
attend_button.pack(pady=(0,20))

# -------------------------------------------------------------------
# Card 3: View Attendance
card3 = ttk.Frame(main_frame, relief="ridge", borderwidth=2)
card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
# Load view attendance image
try:
    view_image = Image.open("UI_Image/verifyy.png")
    view_image = view_image.resize((200, 200), Image.LANCZOS)
    view_photo = ImageTk.PhotoImage(view_image)
    view_label = ttk.Label(card3, image=view_photo)
    view_label.image = view_photo
    view_label.pack(pady=(20,10))
except Exception as e:
    print("View Attendance image not found:", e)
view_button = ttk.Button(card3, text="View Attendance", command=lambda: show_attendance.subjectchoose(text_to_speech))
view_button.pack(pady=(0,20))

# Footer Frame for Exit button
footer_frame = ttk.Frame(window)
footer_frame.pack(side=tk.BOTTOM, pady=20)
exit_button = ttk.Button(footer_frame, text="EXIT", command=window.quit)
exit_button.pack()

# New Window for Registering a Student (Taking Image and Training)
def TakeImageUI():
    ImageUI = tk.Toplevel(window)
    ImageUI.title("Register Your Face")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")
    ImageUI.resizable(False, False)
    
    # Header in Toplevel
    top_header = ttk.Frame(ImageUI)
    top_header.pack(fill=tk.X, pady=10)
    header_label = ttk.Label(top_header, text="Register Your Face", style="Header.TLabel")
    header_label.pack()
    
    # Form Frame
    form_frame = ttk.Frame(ImageUI)
    form_frame.pack(padx=20, pady=20, fill=tk.X)
    
    # Enrollment No.
    en_label = ttk.Label(form_frame, text="Enrollment No", font=("Verdana", 14))
    en_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    en_entry = ttk.Entry(form_frame, font=("Verdana", 16))
    en_entry.grid(row=0, column=1, padx=10, pady=10)
    en_entry.config(validate="key", validatecommand=(en_entry.register(testVal), "%P", "%d"))
    
    # Name
    name_label = ttk.Label(form_frame, text="Name", font=("Verdana", 14))
    name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    name_entry = ttk.Entry(form_frame, font=("Verdana", 16))
    name_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Notification area
    notif_label = ttk.Label(form_frame, text="Notification", font=("Verdana", 14))
    notif_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    notif_msg = ttk.Label(form_frame, text="", background="#333333", foreground="yellow",
                          font=("Verdana", 14, "bold"), anchor="center")
    notif_msg.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    
    # Button Frame
    btn_frame = ttk.Frame(ImageUI)
    btn_frame.pack(pady=20)
    
    def take_image():
        en = en_entry.get()
        nm = name_entry.get()
        takeImage.TakeImage(en, nm, haarcasecade_path, trainimage_path, notif_msg, err_screen, text_to_speech)
        en_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
    
    def train_image():
        trainImage.TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, notif_msg, text_to_speech)
    
    take_img_btn = ttk.Button(btn_frame, text="Take Image", command=take_image)
    take_img_btn.grid(row=0, column=0, padx=20, pady=10)
    
    train_img_btn = ttk.Button(btn_frame, text="Train Image", command=train_image)
    train_img_btn.grid(row=0, column=1, padx=20, pady=10)

# Start the main application loop
window.mainloop()


