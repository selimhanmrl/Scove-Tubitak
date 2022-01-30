# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 14:29:00 2022

@author: MAHMUT KARAASLAN
"""

from datetime import datetime
import numpy as np
import cv2
import math
import time



color_center = open('color_center.txt', 'r')




class calculator:
    def __init__(self):
        self.center_array = []
        self.time_node = datetime.now()
        self.total_path = 0
        self.speed = 0
        
        
    def speed_calc(self):
        
        if (datetime.now()-self.time_node).total_seconds() >=0.5 :
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
        # self.draw_line(frame)
        
        # cv2.putText(frame, " Total path : "+str(self.total_path/1000), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
        # cv2.putText(frame, " Speed : "+str(self.speed), (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0,255),3)
        # cv2.rectangle(frame,(75, 56),(550, 450),(0,0,0),2)
        # if(self.roi_cal(center,(75, 56,550, 450))):
        #     cv2.putText(frame, " Location : Center", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)    
        # else:   
        #     cv2.putText(frame, " Location : Edge", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)    

cap = cv2.VideoCapture("kırmızı_trim.mp4") 

calc=calculator()

total_aktif = 0
total_pasif = 0

while True:
    _,frame = cap.read()
    
    frame=cv2.resize(frame,(1080,720))
    time.sleep(0.01)
    color_line = eval(color_center.readline())
    calc.main(color_line,frame)
    print(calc.speed)
    if calc.speed > 0:
        # print("asd")
        total_aktif = total_aktif +1
        cv2.putText(frame, f" Total Aktif Duvar Kesfi {total_aktif/100}", (0, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)
        cv2.putText(frame, f" Total Pasif Duvar Kesfi {total_pasif/100}", (0, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)
    elif calc.speed <=2:
        total_pasif = total_pasif +1
        cv2.putText(frame, f" Total Aktif Duvar Kesfi {total_aktif/100}", (0, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)
        cv2.putText(frame, f" Total Pasif Duvar Kesfi {total_pasif/100}", (0, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)    
   
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

    