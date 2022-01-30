# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 23:05:22 2022

@author: MAHMUT KARAASLAN
"""

import cv2
import numpy as np
from shapely.geometry import Point, Polygon
import time
import math
from datetime import datetime
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

detecttion_center = open('detection_center.txt', 'r')
roi_file = open('roi.txt', 'r')

roi_line = eval(roi_file.readline())
# print(roi_line)
cap = cv2.VideoCapture("dog.mp4")
# cap = cv2.VideoCapture(0)


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
   
area = Polygon(roi_line)
print(area)
calc=calculator()
total_aktif = 0
total_pasif = 0 
while True:
    _,frame = cap.read()
    
    frame=cv2.resize(frame,(1080,720))
    roi_frame(frame, roi_line)
    detection_line = eval(detecttion_center.readline())
    time.sleep(0.01)
    # print(detection_line)
    # result = cv2.pointPolygonTest(np.array(roi_line, np.int32), (detection_line), False)
    p = Point(detection_line)
    # cv2.circle(frame, detection_line, 4, (0, 0,255), -1)
    
    calc.main(detection_line,frame)
    if not detection_line == (0,0):
        
        if not p.within(area):
            cv2.putText(frame, " Location : Kenar kesfi", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
            
            if calc.speed >2:
                # print("asd")
                total_aktif = total_aktif +1
                cv2.putText(frame, f" Total Aktif Duvar Kesfi {total_aktif/100}", (0, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)
                cv2.putText(frame, f" Total Pasif Duvar Kesfi {total_pasif/100}", (0, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)
            elif calc.speed <=2:
                total_pasif = total_pasif +1
                cv2.putText(frame, f" Total Aktif Duvar Kesfi {total_aktif/100}", (0, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)
                cv2.putText(frame, f" Total Pasif Duvar Kesfi {total_pasif/100}", (0, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)    
        
        else:    
            cv2.putText(frame, " Location : Merkezde", (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
            
            cv2.putText(frame, f" Total Aktif Duvar Kesfi {total_aktif/100}", (0, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)
            cv2.putText(frame, f" Total Pasif Duvar Kesfi {total_pasif/100}", (0, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),3)    
    
    


    
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
    