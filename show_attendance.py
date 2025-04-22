import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
import csv

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

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return

        filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
        newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

        # Create attendance display window
        root = tk.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background=COLORS['bg'])
        
        # Create main frame
        main_frame = tk.Frame(root, bg=COLORS['bg'])
        main_frame.pack(padx=20, pady=20)

        # Header
        header = tk.Label(
            main_frame,
            text=f"Attendance Report - {Subject}",
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            font=("Helvetica Neue", 16, "bold"),
            pady=10,
            width=40
        )
        header.pack(fill=X, pady=(0, 20))

        # Table frame
        table_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        table_frame.pack()

        cs = f"Attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            for r, col in enumerate(reader):
                for c, row in enumerate(col):
                    label = tk.Label(
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

        root.mainloop()
        print(newdf)

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
        text="Which Subject of Attendance?",
        bg=COLORS['primary'],
        fg=COLORS['text_light'],
        font=("Helvetica Neue", 24, "bold"),
        pady=15
    ).pack()

    # Content Frame
    content_frame = tk.Frame(subject, bg=COLORS['bg'])
    content_frame.pack(fill=BOTH, expand=True, padx=40, pady=20)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

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
        fg=COLORS['text'],
        relief='flat',
        highlightthickness=1,
        highlightbackground="#e0e0e0",
        highlightcolor=COLORS['primary']
    )
    tx.pack(pady=(0,20))

    # Buttons Frame
    button_frame = tk.Frame(content_frame, bg=COLORS['bg'])
    button_frame.pack(pady=20)

    def create_button(text, command, width=12):
        btn = tk.Button(
            button_frame,
            text=text,
            command=command,
            font=("Helvetica Neue", 12),
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            relief='flat',
            cursor='hand2',
            width=width,
            pady=8
        )
        
        def on_enter(e):
            btn['background'] = '#1976D2'
        def on_leave(e):
            btn['background'] = COLORS['primary']
            
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn

    # Create and pack buttons
    view_btn = create_button("View Attendance", calculate_attendance)
    view_btn.pack(side=LEFT, padx=10)

    check_btn = create_button("Check Sheets", Attf)
    check_btn.pack(side=LEFT, padx=10)

    subject.mainloop()
