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

haarcasecade_path = "E:\\project-III\\haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "E:\\project-III\\TrainingImageLable\\Trainner.yml"
)
trainimage_path = "E:\project-III\\TrainingImage"
studentdetail_path = (
    "E:\\project-III\\StudentDetails\\studentdetails.csv"
)
attendance_path = "E:\\project-III\\Attendance"
# for choose subject and fill attendance
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
                    e = "Model not found,please train model"
                    Notifica.configure(
                        text=e,
                        bg="#ADD8E6",
                        fg="black",
                        width=33,
                        font=("times", 15, "bold"),
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
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            # En='1604501160'+str(Id)
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                print(aa)
                # attendance["date"] = date
                # attendance["Attendance"] = "P"
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                # fileName = "Attendance/" + Subject + ".csv"
                path = os.path.join(attendance_path, Subject)
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
                    bg="#ADD8E6",
                    fg="black",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)

                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="#ADD8E6")
                cs = os.path.join(path, fileName)
                print(cs)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:

                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="black",
                                font=("times", 15, " bold "),
                                bg="white",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)
            except:
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    ###windo is frame for subject chooser
    subject = Tk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="#ADD8E6")
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(subject, bg="#ADD8E6", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="black",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="#ADD8E6",
        fg="black",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="#ADD8E6",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(
                f"E:\project-III\\Attendance\\{sub}"
            )

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="white",
        fg="black",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject \n ML ,\n DS ,\n AI,\n MP)",
        width=15,
        height=6,
        bg="white",
        fg="black",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 10),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="white",
        fg="black",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="white",
        fg="black",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()


# def subjectChoose(text_to_speech):
#     def FillAttendance():
#         sub = tx.get()
#         if sub == "":
#             t = "Please enter the subject name!!!"
#             text_to_speech(t)
#             return

#         # Verify paths
#         if not os.path.exists(studentdetail_path):
#             print("Error: Student details file not found.")
#             text_to_speech("Student details file not found.")
#             return

#         if not os.path.exists(trainimagelabel_path):
#             print("Error: Model not found. Please train the model.")
#             text_to_speech("Model not found. Please train the model.")
#             return

#         # Load recognizer and face cascade
#         recognizer = cv2.face.LBPHFaceRecognizer_create()
#         recognizer.read(trainimagelabel_path)

#         facecasCade = cv2.CascadeClassifier(haarcasecade_path)

#         # Load student details
#         df = pd.read_csv(studentdetail_path)
#         print("Student details loaded:", df.head())

#         attendance = pd.DataFrame(columns=["Enrollment", "Name"])

#         # Video capture
#         cam = cv2.VideoCapture(0)
#         future = time.time() + 20  # Stop after 20 seconds

#         while time.time() < future:
#             ret, im = cam.read()
#             if not ret:
#                 print("Failed to capture image from camera.")
#                 break

#             gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#             faces = facecasCade.detectMultiScale(gray, 1.2, 5)

#             if len(faces) == 0:
#                 print("No faces detected.")
#                 continue

#             for (x, y, w, h) in faces:
#                 Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
#                 print(f"Detected ID: {Id}, Confidence: {conf}")

#                 if conf < 70:
#                     if Id in df["Enrollment"].values:
#                         name = df.loc[df["Enrollment"] == Id, "Name"].values[0]
#                         attendance.loc[len(attendance)] = [Id, name]
#                         cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 4)
#                         cv2.putText(
#                             im,
#                             f"{Id}-{name}",
#                             (x, y - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             0.8,
#                             (255, 255, 255),
#                             2,
#                         )
#                     else:
#                         print(f"ID {Id} not found in student details.")
#                 else:
#                     cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 4)
#                     cv2.putText(
#                         im,
#                         "Unknown",
#                         (x, y - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX,
#                         0.8,
#                         (0, 0, 255),
#                         2,
#                     )

#             cv2.imshow("Attendance", im)
#             if cv2.waitKey(30) & 0xFF == 27:
#                 break

#         cam.release()
#         cv2.destroyAllWindows()

#         if attendance.empty:
#             print("No valid attendance recorded.")
#             text_to_speech("No valid attendance recorded.")
#             return

#         # Save attendance
#         path = os.path.join(attendance_path, sub)
#         if not os.path.exists(path):
#             os.makedirs(path)

#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         file_path = os.path.join(path, f"{sub}_{timestamp}.csv")
#         attendance.to_csv(file_path, index=False)
#         print("Attendance saved at:", file_path)

#         # Notify user and display attendance
#         m = f"Attendance filled successfully for {sub}"
#         Notifica.configure(
#             text=m,
#             bg="black",
#             fg="yellow",
#             width=33,
#             relief=RIDGE,
#             bd=5,
#             font=("times", 15, "bold"),
#         )
#         text_to_speech(m)
#         Notifica.place(x=20, y=250)

#         root = tk.Tk()
#         root.title(f"Attendance of {sub}")
#         root.configure(background="black")
#         with open(file_path, newline="") as file:
#             reader = csv.reader(file)
#             for r, col in enumerate(reader):
#                 for c, row in enumerate(col):
#                     label = tk.Label(
#                         root,
#                         text=row,
#                         width=10,
#                         height=1,
#                         fg="yellow",
#                         bg="black",
#                         font=("times", 15, "bold"),
#                         relief=tk.RIDGE,
#                     )
#                     label.grid(row=r, column=c)
#         root.mainloop()

#     def Attf():
#         sub = tx.get()
#         if sub == "":
#             t = "Please enter the subject name!!!"
#             text_to_speech(t)
#         else:
#             folder_path = os.path.join(attendance_path, sub)
#             if os.path.exists(folder_path):
#                 os.startfile(folder_path)
#             else:
#                 t = f"No attendance records found for {sub}."
#                 text_to_speech(t)

#     ### Window for subject chooser
#     subject = Tk()
#     subject.title("Subject...")
#     subject.geometry("580x320")
#     subject.resizable(0, 0)
#     subject.configure(background="black")

#     titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
#     titl.pack(fill=X)
#     titl = tk.Label(
#         subject,
#         text="Enter the Subject Name",
#         bg="black",
#         fg="green",
#         font=("arial", 25),
#     )
#     titl.place(x=160, y=12)

#     Notifica = tk.Label(
#         subject,
#         text="Attendance filled Successfully",
#         bg="yellow",
#         fg="black",
#         width=33,
#         height=2,
#         font=("times", 15, "bold"),
#     )

#     attf = tk.Button(
#         subject,
#         text="Check Sheets",
#         command=Attf,
#         bd=7,
#         font=("times new roman", 15),
#         bg="black",
#         fg="yellow",
#         height=2,
#         width=10,
#         relief=RIDGE,
#     )
#     attf.place(x=360, y=170)

#     sub = tk.Label(
#         subject,
#         text="Enter Subject \n (TOC ,\n IWT ,\n CYBER SECURITY,\n DBMS)",
#         width=15,
#         height=6,
#         bg="black",
#         fg="yellow",
#         bd=5,
#         relief=RIDGE,
#         font=("times new roman", 10),
#     )
#     sub.place(x=50, y=100)

#     tx = tk.Entry(
#         subject,
#         width=15,
#         bd=5,
#         bg="white",
#         fg="black",
#         relief=RIDGE,
#         font=("times", 30, "bold"),
#     )
#     tx.place(x=190, y=100)

#     fill_a = tk.Button(
#         subject,
#         text="Fill Attendance",
#         command=FillAttendance,
#         bd=7,
#         font=("times new roman", 15),
#         bg="black",
#         fg="yellow",
#         height=2,
#         width=12,
#         relief=RIDGE,
#     )
#     fill_a.place(x=195, y=170)
#     subject.mainloop()
