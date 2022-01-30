# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 10:26:42 2022

@author: MAHMUT KARAASLAN
"""

from color_detection import color_detection
import cv2
import numpy as np

f = open('color_center.txt', 'w')

cap = cv2.VideoCapture("yan_trim.mp4")     
             
roi_file = open('roi.txt', 'r')
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
detection=color_detection()
total=0
while True:
    try:
        _,frame = cap.read()
        total = total+1
        frame = cv2.resize(frame,(1080,720))
        # frame=roi_frame(frame,pts)
        
        # frame = cv2.resize(frame,(800,600))
        center=detection.processes(frame)
        f.write(str(center)+"\n")
        # print(center)
        
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        break
print(total)    
f.close()    
cap.release() 
cv2.destroyAllWindows() 