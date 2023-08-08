import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import mysql.connector
from datetime import datetime,timedelta

import pandas as pd
from tkinter import *
# from tkinter import ttk
from PIL import Image,ImageTk
from check_attendance import attendance
# import tkinter as tk

class Face_rec_sys:
    def __init__(self,root):
        # window=tk.Tk()
        # width= window.winfo_screenwidth()
        # height= window.winfo_screenheight()
        self.root = root
        # window.geometry("%dx%d" % (width, height))
        self.root.geometry("1000x700")
        self.root.title("FACE RECOGNITION ATTENDANCE SYSTEM")

        imgm=Image.open(r'imagem\first.jpg')
        imgm =imgm.resize((500,130),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(imgm)

        firstlabel = Label(self.root,image=self.photoimg)
        firstlabel.place(x=0,y=0,width=500,height=130)

        imgm1=Image.open('imagem\second.jpg')
        imgm1 =imgm1.resize((500,130),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(imgm1)

        firstlabel = Label(self.root,image=self.photoimg1)
        firstlabel.place(x=500,y=0,width=500,height=130)

        imgmbg=Image.open(r'imagem\backg.jpg')
        imgmbg =imgmbg.resize((1000,700),Image.Resampling.LANCZOS)
        self.photoimgbg=ImageTk.PhotoImage(imgmbg)

        firstlabel = Label(self.root,image=self.photoimgbg)
        firstlabel.place(x=0,y=130,width=1000,height=700)

        title_lbl = Label(text="FACE RECOGNITION ATTENDANCE SYSTEM",font=("times new roman",25,"bold"),bg='black',fg='white')
        title_lbl.place(x=0,y=130,width=1000,height=35)

        imgmark=Image.open(r'imagem\button1.png')
        imgmark =imgmark.resize((180,180),Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(imgmark)

        b1 = Button(image=self.photoimg3,cursor="hand2",command=self.face_rec_att)
        b1.place(x=450,y=280,width=180,height=180)

        b1_1 = Button(text="MARK ATTENDANCE",cursor="hand2")
        b1_1.place(x=450,y=450,width=180,height=30)

        imgcheck=Image.open(r'imagem\button21.jpg')
        imgcheck =imgcheck.resize((180,180),Image.Resampling.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(imgcheck)

        b2 = Button(image=self.photoimg4,cursor="hand2",command=self.attendance)
        b2.place(x=680,y=280,width=180,height=180)

        b2_2 = Button(text="CHECK ATTENDANCE",cursor="hand2",command=self.attendance)
        b2_2.place(x=680,y=450,width=180,height=30)

    def attendance(self):
        self.new_window=Toplevel(self.root)
        self.app=attendance(self.new_window)  
        
    
    def face_rec_att(self):

        conn = mysql.connector.connect(host='localhost', username='root', password='Pr@bh123', database='data face reco')
        my_cursor = conn.cursor()

        



        font = cv2.FONT_HERSHEY_DUPLEX

        cap = cv2.VideoCapture(0)
        cap.set(3,640)
        cap.set(4,480)

        imgbg=cv2.imread('background.jpg')
        modetype=0
        counter=0
        id=-1
        matchindex=0

        folderpath= 'Images1'
        pathlist=os.listdir(folderpath)
        imglist={}
        for path in pathlist:
            imgorig = cv2.imread(os.path.join(folderpath, path))
            img_id = os.path.splitext(path)[0]  # Get the student ID from the filename
            imglist[img_id] = imgorig

        new_imglist = {}

        for img_id, img_orig in imglist.items():
            # orig_height, orig_width, _ = img_orig.shape
            # resize the image
            new_height, new_width = 150, 150
            img_resized = cv2.resize(img_orig, (new_height, new_width))
            # add the resized image to the new dictionary
            new_imglist[img_id] = img_resized


        folderModepath= 'Modes'
        modepathlist=os.listdir(folderModepath)
        imgmodelist = []
        for path in modepathlist:
            imgmodelist.append(cv2.imread(os.path.join(folderModepath,path)))

        #load encoding file
        file = open('encodefile.p','rb')
        encodelistknownwithids = pickle.load(file)
        file.close()
        encodelistknown,studentids = encodelistknownwithids

        # total_attendance =0


        while True:
            

                success, img = cap.read()
                img_resized = cv2.resize(img, (517, 360))
                imgbg[218:218+360,140:140+517] = img_resized
                # imgbg[160:160+480,50:50+640] = img
            
                
                

            

                imgS = cv2.resize(img_resized, (0, 0), None, 0.25, 0.25)
                
                
                facecurframe = face_recognition.face_locations(imgS)
                encodecurframe = face_recognition.face_encodings(imgS,facecurframe)
                def mark_attendance(n,c,u,b,y):
                    conn = mysql.connector.connect(host='localhost', username='root', password='Pr@bh123', database='data face reco')
                    my_cursor = conn.cursor()

          
                    my_cursor.execute("SELECT * FROM attendance WHERE crn =" + str(id))

                    # Fetch the results and check if there are any rows returned
                    result1 = my_cursor.fetchone()
                    if result1:
                        my_cursor.execute("SELECT * FROM attendance")
                        result = my_cursor.fetchall()
                        for record in result:
                            last_updated_datetime = datetime.combine(datetime.strptime(record[5], '%d/%m/%Y'), datetime.strptime(record[6], '%H:%M:%S').time())


                            elapsed_time = datetime.now() - last_updated_datetime

                            if elapsed_time >= timedelta(hours=1):
                                new_total_attendance = int(record[8]) + 1

                                now = datetime.now()
                                d1 = now.strftime("%d/%m/%Y")
                                dtstring = now.strftime("%H:%M:%S")
                                sql = "UPDATE attendance SET  date = %s, time = %s, total_att=%s WHERE crn = %s"
                                data = ( d1, dtstring,new_total_attendance, id)
                                my_cursor.execute(sql, data)
                                conn.commit()


                    else:            

                        conn=mysql.connector.connect(host='localhost',username='root',password='Pr@bh123',database='data face reco')
                        my_cursor=conn.cursor()
                    
                        sql = "INSERT INTO attendance (crn, urn, name, branch, year, date, time, status,total_att) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,1)"

                        now=datetime.now()
                        d1=now.strftime("%d/%m/%Y")
                        dtstring=now.strftime("%H:%M:%S")
                        
                        data=(c,u,n,b,y,d1,dtstring,"Present")

                        my_cursor.execute(sql, data)

                        conn.commit()

                    
                        

            
                
                
                
            
                imgbg[160:160+478,788:788+368] = imgmodelist[modetype]
                if facecurframe:
                    
                    for encodeface,faceloc in zip(encodecurframe,facecurframe):
                        matches = face_recognition.compare_faces(encodelistknown,encodeface,tolerance=0.5)
                        facedis = face_recognition.face_distance(encodelistknown,encodeface)

                        matchindex = np.argmin(facedis)
                    # print('match index',matchindex)

                        if matches[matchindex]:
                        # print('known face detected')
                            # print(studentids[matchindex])
                            y1, x2, y2, x1 = faceloc
                            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                            bbox = 140 + x1, 218 + y1, x2 - x1, y2 - y1
                            imgbg = cvzone.cornerRect(imgbg,bbox,rt=0)


                            conn=mysql.connector.connect(host='localhost',username='root',password='Pr@bh123',database='data face reco')
                            my_cursor=conn.cursor()

                            my_cursor.execute("select Name from student_data where CRN="+str(studentids[matchindex]))
                            n=my_cursor.fetchone()
                            n="+".join(n)

                            my_cursor.execute("select CRN from student_data where CRN="+str(studentids[matchindex]))
                            c=my_cursor.fetchone()
                            c="+".join(c)

                            my_cursor.execute("select URN from student_data where CRN="+str(studentids[matchindex]))
                            u=my_cursor.fetchone()
                            u="+".join(u)

                            my_cursor.execute("select Branch from student_data where CRN="+str(studentids[matchindex]))
                            b=my_cursor.fetchone()
                            b="+".join(b)

                            my_cursor.execute("select year from student_data where CRN="+str(studentids[matchindex]))
                            y=my_cursor.fetchone()
                            y="+".join(y)

                            id=studentids[matchindex]
                            
                            if counter ==0:
                                
                                # cvzone.putTextRect(imgbg, "Loading", (275, 400))
                                cv2.imshow("Face Attendance", imgbg)
                                cv2.waitKey(1)
                    
                                counter=1
                                modetype =1
                        
                        else:
                            cv2.putText(imgbg, 'Unknown face detected!', (200,300), font, 1.0, (255, 255, 255), 1)

                
                    if counter !=0:
                        
                        
                        
                
                        if id in imglist:
                                imgorig1=new_imglist[id]

                        if 5<counter <20:
                            
                            my_cursor.execute("SELECT * FROM attendance WHERE crn ="+str (id))
                            result = my_cursor.fetchone()
                            if result:
    # Get the last updated datetime from the result
                                last_updated_datetime = datetime.combine(datetime.strptime(result[5], '%d/%m/%Y'), datetime.strptime(result[6], '%H:%M:%S').time())

                                # Calculate the elapsed time since last update
                                elapsed_time = datetime.now() - last_updated_datetime

                                if elapsed_time <= timedelta(hours=1):
                                    # If the elapsed time is less than or equal to 1 hour,
                                    # set the mode type to 3 (already marked as present)
                                    modetype = 3
                                else:
                                    # Otherwise, mark the attendance and set the mode type to 2 (marked as present)
                                    mark_attendance(n, c, u, b, y)
                                    modetype = 2

                                    # Get the old date and time from the result
                                    old_datetime = (result[5], result[6])

                                    # Backup the old date and time to the backup table
                                    if old_datetime:
                                        backup_data = (id, old_datetime[0], old_datetime[1])
                                        backup_query = "INSERT INTO attendance_backup (CRN, Date, Time) VALUES (%s, %s, %s)"
                                        my_cursor.execute(backup_query, backup_data)
                                        conn.commit()
                            else:
                                # If no record found, mark the attendance and set the mode type to 2 (marked as present)
                                mark_attendance(n, c, u, b, y)
                                modetype = 2

                        imgbg[160:160+478,788:788+368] = imgmodelist[modetype]

                        if modetype!=3:
                        
                            if counter<=5:
                                cv2.putText(imgbg,str(n),(900,458),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
                                cv2.putText(imgbg,str(c),(965,485),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                                cv2.putText(imgbg,str(b),(965,528),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                                cv2.putText(imgbg,str(y),(965,570),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                                imgbg[275:275+150,895:895+150] = imgorig1
                        
                        
                
                        counter+=1

                        if counter>=20:
                            counter = 0
                            modetype=0
                            imgbg[160:160+478,788:788+368] = imgmodelist[modetype]

                        
                        
                else:
                    modetype=0
                    counter=0

                cv2.imshow("face Attendance", imgbg)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            #cv2.imshow("webcam",img)
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = Face_rec_sys(root)
    root.mainloop()