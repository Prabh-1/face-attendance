from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import os
import csv
from tkinter import filedialog
import mysql.connector
import pandas as pd

mydata=[]

class attendance:
    conn = mysql.connector.connect(host='localhost', username='root', password='Pr@bh123', database='data face reco')
    df = pd.read_sql_query('SELECT * FROM attendance', conn)

# Write the rows to a CSV file without including the column names
    df.to_csv('attendance.csv', index=False, header=False)
    def __init__(self,root):
        self.root=root
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

        main_frame = Frame(firstlabel, bd=2, bg="white")
        main_frame.place(x=50, y=100, width=900, height=400)

        frame2=LabelFrame(main_frame,bd=2,bg='white',relief=RIDGE,text='Attendance details',font=('times new roman',15))
        frame2.place(x=55,y=90,width=800,height=250)

        import_btn=Button(main_frame,text='Import CSV',command=self.importcsv,width=17,font=('times new roman',13,'bold'),bg="blue",fg='white')
        import_btn.place(x=380,y=40,width=180,height=30)

        table_frame=Frame(frame2,bd=2,relief=RIDGE,bg="white")
        table_frame.place(x=5,y=5,width=782,height=213)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.attendancereporttable=ttk.Treeview(table_frame,column=("CRN","URN","Name","Branch","Year","Date","Time","Status","Total Attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.attendancereporttable.xview)
        scroll_y.config(command=self.attendancereporttable.yview)

        self.attendancereporttable.heading("CRN",text="CRN")
        self.attendancereporttable.heading("URN",text="URN")
        self.attendancereporttable.heading("Name",text="Name")
        self.attendancereporttable.heading("Branch",text="Branch")
        self.attendancereporttable.heading("Year",text="Year")
        self.attendancereporttable.heading("Date",text="Date")
        self.attendancereporttable.heading("Time",text="Time")
        self.attendancereporttable.heading("Status",text="Status")
        self.attendancereporttable.heading("Total Attendance",text="Total Attendance")
        # self.attendancereporttable.heading("Total Attendance",text="Total Attendance")

        self.attendancereporttable["show"]="headings"
        self.attendancereporttable.column("CRN",width=100)
        self.attendancereporttable.column("URN",width=100)
        self.attendancereporttable.column("Name",width=150)
        self.attendancereporttable.column("Branch",width=100)
        self.attendancereporttable.column("Year",width=100)
        self.attendancereporttable.column("Date",width=100)
        self.attendancereporttable.column("Time",width=100)
        self.attendancereporttable.column("Status",width=100)

        self.attendancereporttable.column("Total Attendance",width=100)


    
        self.attendancereporttable.pack(fill=BOTH,expand=1)

    def fetch_data(self,rows):
        self.attendancereporttable.delete(*self.attendancereporttable.get_children())
        for i in rows:
            self.attendancereporttable.insert("",END,values=i)

    def importcsv(self):
        global mydata
        mydata.clear()
        filenm=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("ALl File","*.*")),parent=self.root)
        with open(filenm) as myfile:
            csvread=csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetch_data(mydata)



if __name__ == "__main__":
    root=Tk()
    obj=attendance(root)
    root.mainloop()

    