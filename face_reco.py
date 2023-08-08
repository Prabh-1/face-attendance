import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import mysql.connector
from time import strftime
from datetime import datetime


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
    orig_height, orig_width, _ = img_orig.shape
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




while True:
    

        success, img = cap.read()
        img_resized = cv2.resize(img, (517, 360))
        imgbg[218:218+360,140:140+517] = img_resized
        # imgbg[160:160+480,50:50+640] = img
    
        
        

    

        imgS = cv2.resize(img_resized, (0, 0), None, 0.25, 0.25)
        
        
        facecurframe = face_recognition.face_locations(imgS)
        encodecurframe = face_recognition.face_encodings(imgS,facecurframe)
        def mark_attendance(n,c,u,b,y):
            with open('attendance.csv','r+',newline='\n') as f:
                mydatalist = f.readlines()
                name_list=[]
                # print(name_list)
                for line in mydatalist:
                        entry=line.split((","))
                        name_list.append(entry[0])
                        # print(name_list)
                if((c not in name_list) and (u not in name_list) and (n not in name_list) and (b not in name_list) and (y not in name_list)):
                    now=datetime.now()
                    d1=now.strftime("%d/%m/%Y")
                    dtstring=now.strftime("%H:%M:%S")
                    f.writelines(f"\n{c},{u},{n},{b},{y},{dtstring},{d1},Present")

    
        
        
        
    
        imgbg[160:160+478,788:788+368] = imgmodelist[modetype]
        if facecurframe:
            
            for encodeface,faceloc in zip(encodecurframe,facecurframe):
                matches = face_recognition.compare_faces(encodelistknown,encodeface)
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
                        counter=1
                        modetype =1
        

           
            if counter !=0:
                
                
        
                if id in imglist:
                        imgorig1=new_imglist[id]

                if 5<counter <20:
                    with open('attendance.csv','r+',newline='\n') as f:
                        mydatalist = f.readlines()
                        name_list=[]
                        # print(name_list)
                        for line in mydatalist:
                                entry=line.split((","))
                                name_list.append(entry[0])
                    if((c not in name_list) and (u not in name_list) and (n not in name_list) and (b not in name_list) and (y not in name_list)):
                        modetype=2
                    else:
                        modetype=3
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

                mark_attendance(n,c,u,b,y)
        else:
             modetype=0
             counter=0

        cv2.imshow("face Attendance", imgbg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #cv2.imshow("webcam",img)

cap.release()
cv2.destroyAllWindows()
