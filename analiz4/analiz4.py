# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 20:22:42 2022

@author: MAHMUT KARAASLAN
"""

import cv2
import numpy as np
import math
from datetime import datetime
import time



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
 

# roi_file = open('roi.txt', 'r')
detecttion_center = open('detection_center.txt', 'r')
color_center = open('color_center.txt', 'r')
cap = cv2.VideoCapture("yan_trim.mp4")

total_kesif = 0
total_stabil = 0
total_aktif = 0
total_pasif = 0
calc=calculator()

while True:
    try:
        
        _,frame = cap.read()
        frame= cv2.resize(frame,(1080,720))
        
        time.sleep(0.01)
        
        detection_line = eval(detecttion_center.readline())
        color_line = eval(color_center.readline())
        
        calc.main(color_line,frame)
        
        # cv2.circle(frame, color_line, 5, (0, 0, 255), -1)
        
        distance=math.sqrt((color_line[0]-detection_line[0])**2 + (color_line[1]-detection_line[1])**2)
        # print(color_line)
        # cv2.putText(frame, " Durum : ", (750, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
        
        print(calc.speed)
        if distance<=250 or color_line == (0,0):
            total_kesif = total_kesif +1
            
            # cv2.putText(frame, "Kesfediyor ", (450, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
            
            # cv2.putText(frame, f"Total Stabil : {total_stabil/100} ", (550, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),3)
            # cv2.putText(frame, f"Total Wobbler Kesfi : {total_kesif/100}", (550, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)
            # print(detection_line)
            if calc.speed > 0.8 or color_line == (0,0):
                # print("asd")
                total_aktif = total_aktif +1
                cv2.putText(frame, f" Total Wobbler Oynama {total_aktif/100}", (550, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)
                cv2.putText(frame, f" Total Wobbler Kesfi {total_pasif/100}", (550, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)
            elif calc.speed <=0.8 :
                total_pasif = total_pasif +1
                cv2.putText(frame, f" Total Wobbler Oynama {total_aktif/100}", (550, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)
                cv2.putText(frame, f" Total Wobbler Kesfi {total_pasif/100}", (550, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)    
           
           
            
            # cv2.line(frame, detection_line, color_line, color=(0, 255, 0), thickness=2)
        else:
            total_stabil = total_stabil + 1
            # cv2.putText(frame, "Stabil", (450, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2)
            
            # cv2.putText(frame, f"Total Stabil : {total_stabil/100} ", (550, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)
            # cv2.putText(frame, f"Total Wobbler Kesfi : {total_kesif/100}", (550, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),3)
            cv2.putText(frame, f" Total Wobbler Oynama {total_aktif/100}", (550, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)
            cv2.putText(frame, f" Total Wobbler Kesfi {total_pasif/100}", (550, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)    
      
           
            # cv2.line(frame, detection_line, color_line, color=(0, 0, 255), thickness=2)
        
        
  
        
        
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print("asf")
        break
      
detecttion_center.close()
color_center.close()
cap.release()
cv2.destroyAllWindows()    
