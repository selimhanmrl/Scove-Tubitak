import cv2
import numpy as np
from shapely.geometry import Point, Polygon
from Draw_Polygons import PolygonDrawer
import math

# ***** replace with required image path *****
cap = cv2.VideoCapture('a.mp4')

# ***** global variable decleration *****
_, frame1 = cap.read()
_, frame2 = cap.read()

# Back Graund Substraction
backSub = cv2.createBackgroundSubtractorKNN(detectShadows=False)

roi = cv2.selectROI(frame1, showCrosshair=False, fromCenter=False)
(x1,y1,w1,h1) = roi

#roi = (239, 200, 117, 114)

## Polygon Drawer Class
pd = PolygonDrawer("Polygon",frame1)
image = pd.run(frame1)

#fps for calculate time
fps = cap.get(5)
pts = []
print(pd.points)

#pd.points = [[(347, 205), (541, 209), (541, 249), (346, 249)], [(302, 247), (307, 208), (113, 203), (111, 239)], [(315, 45), (347, 44), (347, 207), (311, 211)], [(307, 431), (341, 429), (309, 253), (344, 253)]]

# for plus maze there is 4 polygon to separate experimant area
polyRight = Polygon(pd.points[0])

polyleft = Polygon(pd.points[1])

polyUp = Polygon(pd.points[2])

polyDown = Polygon(pd.points[3])

#polyMid = Polygon(pd.points[4])
framecounts = []
framecount = 0
flag = 0
times = []
total_path=0
count = 0
while cap.isOpened():

    frame1 = frame1[y1:y1+h1, x1:x1+w1]
    frame2 = frame2[y1:y1+h1, x1:x1+w1]
    # Here is tracking methods  with order : backgraund subsraction - threshold - dilate - find contours
    mask = backSub.apply(frame1)
    #diff = cv2.absdiff(frame1, frame2)
    _,thresh = cv2.threshold(mask,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,None,iterations=3)
    _,contours,_ = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # here find biggest contour and draw rectangle around it after find center point and check if that point in polygons which we describe or not and count how many second there
    for contour in contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        #(x,y,w,h) = cv2.boundingRect(contour)


        if cv2.contourArea(contour) <700:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        M = cv2.moments(contour)

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        center = (cx, cy)

        if count > 60:
            pts.append(center)
        frame1 = cv2.circle(frame1, center, 5, (0, 0, 255), -1)
        p = Point(cx, cy)
        if p.within(polyRight):
             cv2.putText(frame1, " Sag Tarafta " + str(framecount/fps), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
             framecount += 1
             flag = 1
        elif p.within(polyleft):
             cv2.putText(frame1, " Sol Tarafta "+ str(framecount/fps), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
             flag = 2
             framecount += 1
        elif p.within(polyUp):
             cv2.putText(frame1, " Yukari Tarafta ", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
             flag = 3
             framecount += 1
        elif p.within(polyDown):
             cv2.putText(frame1, " Asagi Tarafta ", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
             flag = 4
             framecount += 1
        else:
              cv2.putText(frame1, " Orta Noktada ", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
              if (framecount > (2*fps)):
                framecounts = (framecount/fps, flag)
                times.append(framecounts)
                framecount = 0
                flag = 0
        count +=1
    if len(pts)>1:
        for i in range(len(pts)-1):
            cv2.line(frame1,pts[i],pts[i+1],(0,0,255),1)

    cv2.imshow('Feed',frame1)
    #cv2.imshow('mask',mask)

    frame1 = frame2
    ret,frame2 = cap.read()


    key = cv2.waitKey(1)
    if key == 27:
        break
# Measure tracked path    
for i in range(len(pts)-1):
    dist = math.sqrt((pts[i+1][0] - pts[i][0])**2 + (pts[i+1][1] - pts[i][1])**2)
    total_path+=dist

print(total_path)
print(times)
cap.release()
cv2.destroyAllWindows()
