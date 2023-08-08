import cv2
import face_recognition
import pickle
import os

folderpath= 'Images1'
pathlist=os.listdir(folderpath)

imglist = []
studentids= []
for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
    studentids.append(os.path.splitext(path)[0])
    # print(imglist)


def findencodings(imageslist):
    encodelist =[]
    for img in imageslist:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    
    return encodelist
print('encoding started')
print(findencodings(imglist))
encodelistknown = findencodings(imglist)
encodelistknownwithids=[encodelistknown,studentids]
print("encoding complete")

file=open('encodefile.p','wb')
pickle.dump(encodelistknownwithids,file)
file.close()
print('file saved')