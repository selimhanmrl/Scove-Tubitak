# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 09:59:37 2022

@author: MAHMUT KARAASLAN
"""

import cv2
import numpy as np




class color_detection:
    def __init__(self):
        self.lowerBound = np.array([170, 110, 100])          #RASP
        self.upperBound = np.array([179, 255, 230])
        self.kernelOpen=np.ones((5,5))
        self.kernelClose=np.ones((20,20))
        self.Mx=0
        self.My=0
        
    def processes(self,frame):
        
    
            imgHSV= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mask=cv2.inRange(imgHSV,self.lowerBound,self.upperBound)
            maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,self.kernelOpen)
            maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,self.kernelClose)
            maskFinal=maskClose
            conts, _= cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
               
            if len(conts) != 0:
                c = max(conts, key = cv2.contourArea)
                x,y,w,h = cv2.boundingRect(c)
                try:   
                    (self.Mx,self.My),radius = cv2.minEnclosingCircle(c)
                    center = (int(self.Mx),int(self.My))
                    radius = int(radius)
                        
                        # img = cv2.circle(img,center,2,(255,255,255),2)
                    if (w+h > 10):
                        frame = cv2.circle(frame,center,radius,(0,255,0),2)
                        cv2.circle(frame,(int(self.Mx),int(self.My)), 2, (0,255,255), -1)
                                                    #print("X" + str(self.Mx) + " -- Y" + str(self.My))
                    else: 
                        self.Mx=0
                        self.My=0
                except:
                    print("hata")
            else:
                self.Mx = 0
                self.My = 0
            center = (int(self.Mx),int(self.My))
            return center                    

   
             