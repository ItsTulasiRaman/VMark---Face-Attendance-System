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
import tkinter.ttk as tkk
import tkinter.font as font

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

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel\\Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails\\studentdetails.csv"
attendance_path = "Attendance"

def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found, please train model"
                    Notifica.configure(
                        text=e,
                        bg=COLORS['surface'],
                        fg=COLORS['error'],
                        width=33,
                        font=("Helvetica Neue", 12)
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [Id, aa]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                print(aa)
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                print(attendance)
                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg=COLORS['surface'],
                    fg=COLORS['primary'],
                    width=33,
                    relief='flat',
                    font=("Helvetica Neue", 12)
                )
                text_to_speech(m)
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background=COLORS['bg'])
                
                # Create a frame for the table
                table_frame = tkinter.Frame(root, bg=COLORS['bg'])
                table_frame.pack(padx=20, pady=20)
                
                cs = os.path.join(path, fileName)
                print(cs)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(
                                table_frame,
                                width=15,
                                height=2,
                                fg=COLORS['text'],
                                font=("Helvetica Neue", 12),
                                bg=COLORS['surface'] if r % 2 == 0 else COLORS['bg'],
                                text=row,
                                relief='flat'
                            )
                            label.grid(row=r, column=c, padx=2, pady=2)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)
            except:
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    # Subject Window
    subject = Tk()
    subject.title("Subject Selection")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background=COLORS['bg'])

    # Header Frame
    header_frame = tk.Frame(subject, bg=COLORS['primary'])
    header_frame.pack(fill=X)

    # Title
    tk.Label(
        header_frame,
        text="Enter the Subject Name",
        bg=COLORS['primary'],
        fg=COLORS['text_light'],
        font=("Helvetica Neue", 24, "bold"),
        pady=15
    ).pack()

    # Content Frame
    content_frame = tk.Frame(subject, bg=COLORS['bg'])
    content_frame.pack(fill=BOTH, expand=True, padx=40, pady=20)

    # Notification Label
    Notifica = tk.Label(
        content_frame,
        text="",
        bg=COLORS['surface'],
        fg=COLORS['text'],
        width=33,
        height=2,
        font=("Helvetica Neue", 12)
    )

    # Subject Entry
    tk.Label(
        content_frame,
        text="Enter Subject",
        bg=COLORS['bg'],
        fg=COLORS['text'],
        font=("Helvetica Neue", 14)
    ).pack(pady=(20,5))

    tx = tk.Entry(
        content_frame,
        width=20,
        font=("Helvetica Neue", 14),
        bg=COLORS['surface'],
        relief='flat',
        highlightthickness=1,
        highlightbackground="#e0e0e0",
        highlightcolor=COLORS['primary']
    )
    tx.pack(pady=(0,20))

    # Buttons Frame
    button_frame = tk.Frame(content_frame, bg=COLORS['bg'])
    button_frame.pack(pady=20)

    def create_button(text, command):
        btn = tk.Button(
            button_frame,
            text=text,
            command=command,
            font=("Helvetica Neue", 12),
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            relief='flat',
            cursor='hand2',
            width=15,
            pady=8
        )
        
        def on_enter(e):
            btn['background'] = '#1976D2'
        def on_leave(e):
            btn['background'] = COLORS['primary']
            
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    # Create and pack buttons
    fill_a = create_button("Fill Attendance", FillAttendance)
    fill_a.pack(side=LEFT, padx=10)

    attf = create_button("Check Sheets", Attf)
    attf.pack(side=LEFT, padx=10)

    subject.mainloop()
