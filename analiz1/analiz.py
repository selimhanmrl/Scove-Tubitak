# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 20:22:42 2022

@author: MAHMUT KARAASLAN
"""

import cv2
import numpy as np
import math


cap = cv2.VideoCapture("kırmızı_toplu.mp4")




# roi_file = open('roi.txt', 'r')
detecttion_center = open('detection_center.txt', 'r')
color_center = open('color_center.txt', 'r')

total_kesif = 0
total_stabil = 0


while True:
    try:
        
        _,frame = cap.read()
        frame= cv2.resize(frame,(1080,720))
        
        detection_line = eval(detecttion_center.readline())
        color_line = eval(color_center.readline())

        
        # cv2.circle(frame, detection_line, 5, (0, 0, 255), -1)
        # cv2.circle(frame, color_line, 5, (0, 255, 0), -1)
        distance=math.sqrt((color_line[0]-detection_line[0])**2 + (color_line[1]-detection_line[1])**2)
        print(distance)
        # cv2.putText(frame, " Durum : ", (750, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
        if distance<=135:
            total_kesif = total_kesif +1
            
            # cv2.putText(frame, "Kesfediyor ", (450, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
            
            cv2.putText(frame, f"Total Stabil : {total_stabil/100} ", (550, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),3)
            cv2.putText(frame, f"Total Wobbler Kesfi : {total_kesif/100}", (550, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)
            
           
            
            # cv2.line(frame, detection_line, color_line, color=(0, 255, 0), thickness=2)
        else:
            total_stabil = total_stabil + 1
            # cv2.putText(frame, "Stabil", (450, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2)
            
            cv2.putText(frame, f"Total Stabil : {total_stabil/100} ", (550, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (157, 17, 24),3)
            cv2.putText(frame, f"Total Wobbler Kesfi : {total_kesif/100}", (550, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),3)
            
           
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
