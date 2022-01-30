# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 20:22:42 2022

@author: MAHMUT KARAASLAN
"""
import cv2
import numpy as np
import time
from datetime import datetime
import math
from color_detection import color_detection
largura_min=40 #Largura minima do retangulo
altura_min=40 #Altura minima do retangulo

offset=6 #Erro permitido entre pixel  

pos_linha=150 #Posição da linha de contagem 

delay= 60 #FPS do vídeo

detec = []
carros= 0
# time.sleep(5)
	
def center_cal(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture("yan_trim.mp4")
subtracao = cv2.createBackgroundSubtractorKNN()
total=0
t0=0
t1=0
tutucu=0
reset=datetime.now()
dizi = []
total_path=0
hız=0
old_total=0

roi_file = open('roi.txt', 'r')
detection = open('detection_center.txt', 'w')
pts=roi_file.read()

pts=eval(pts)    
print(pts)


def roi_frame(img,pts):
        mask = np.zeros(img.shape, np.uint8)
        points = np.array(pts, np.int32)
        points = points.reshape((-1, 1, 2))
        mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
        mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255)) # for ROI
        mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0)) # for displaying images on the desktop
 
        show_image = cv2.addWeighted(src1=img, alpha=0.8, src2=mask3, beta=0.2, gamma=0)
        ROI = cv2.bitwise_and(mask2, img)
        cv2.imshow("show_img", show_image)
        return ROI

class calculator:
    def __init__(self):
        self.center_array = []
        self.time_node = datetime.now()
        self.total_path = 0
        self.speed = 0
        
        
    def speed_calc(self):
        
        if (datetime.now()-self.time_node).total_seconds() >=1 :
            self.time_node =datetime.now()
            index = len(self.center_array)-2
            self.speed = math.sqrt((self.center_array[index+1][0] - self.center_array[index][0])**2 + (self.center_array[index+1][1] - self.center_array[index][1])**2)
            
    def draw_line(self,frame):
            
        if len(self.center_array)>1:
            for i in range(len(self.center_array)-1):                        
                cv2.line(frame,self.center_array[i],self.center_array[i+1],(0,0,255),1)    
         
    def total_path_calc(self):
        for i in range(len(self.center_array)-1):
            dist = math.sqrt((self.center_array[i+1][0] - self.center_array[i][0])**2 + (self.center_array[i+1][1] - self.center_array[i][1])**2)
            self.total_path+=dist        
    def roi_cal(self,center,roi):
        if (center[0]>roi[0] and center[1]>roi[1] and center[0]<roi[2] and center[1]<roi[3]):
            # print("içerdema")
            return True
    def main(self,center,frame):
        self.center_array.append(center)
        self.speed_calc()
        self.total_path_calc()
        self.draw_line(frame)
        
        # cv2.putText(frame, " Total path : "+str(self.total_path/1000), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
        cv2.putText(frame, " Speed : "+str(self.speed), (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0,255),3)
        # cv2.rectangle(frame,(75, 56),(550, 450),(0,0,0),2)
        if(self.roi_cal(center,(75, 56,550, 450))):
            cv2.putText(frame, " Location : Center", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)    
        else:   
            cv2.putText(frame, " Location : Edge", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)    
    
        
        
calc=calculator()        
total =0
while True:
    try:
        ret , frame = cap.read()
        frame=cv2.resize(frame,(1080,720))
        frame=roi_frame(frame, pts)
        total = total +1
        frame1=frame.copy()
        
        # rows,cols,ch = frame1.shape
        # M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
        # frame1 = cv2.warpAffine(frame1,M,(cols,rows))    
        
        
        tutucu=0
        # start_time=datetime.now()
        
    
        grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        blur=cv2.medianBlur(grey, ksize=7)
        blur = cv2.GaussianBlur(grey,(3,3),5)
        img_sub = subtracao.apply(blur)
        dilat = cv2.dilate(img_sub,np.ones((5,5)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilatada = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
        dilatada = cv2.morphologyEx (dilatada, cv2. MORPH_CLOSE , kernel)
        contorno,h=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # contorno = max(contorno, key = cv2.contourArea)
        control=0
        for(i,c) in enumerate(contorno):
            c= max(contorno, key = cv2.contourArea)
            (x,y,w,h) = cv2.boundingRect(c)
            
            validar_contour = (w >= largura_min) and (h >= altura_min)
            if not validar_contour:
                continue
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)        
            center = center_cal(x, y, w, h)
            detec.append(center)
            cv2.circle(frame1, center, 4, (0, 0,255), -1)
            cv2.circle(frame, center, 4, (0, 0,255), -1)
            control=1
    
        
        # cv2.rectangle(frame1,(75, 56),(550, 450),(0,0,255),2)
            
        if len(detec)>=10:
            # calc.main(center,frame)            
            print(center)
        
            detection.write(str(center)+"\n")
        else:
            detection.write(str((0,0))+"\n")
        
        # result=np.hstack((frame1,frame))
        # cv2.imshow("Result" , result)
        cv2.imshow("frame" , frame)
        # cv2.imshow("Detectar",frame1)
        
        if cv2.waitKey(1) == 27:
            break
    except:
        break
print(total)    
detection.close()
cv2.destroyAllWindows()
cap.release()
