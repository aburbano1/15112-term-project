import cv2
import numpy as np
import imutils
import os
###
#following code tracks a certain color (spanish orange)
    #then finds coordinates of largest contours
        #then uses these coordinates to create a circle around object 
            #uses coordinates to draw line segment from current pnt to previous
###

#creates range of color to track- current color=m&m wrapper & burts bees chapstick
lower = np.array([7,150,180])
upper = np.array([100,250,250])
points = []
cam = cv2.VideoCapture(0)
count =0
def sideBar(image,cx1,cy1,cx2,cy2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    cv2.rectangle(image,(cx1,cy1),(cx2,cy2//3),(0,0,250), 5)   
    cv2.rectangle(image,(cx1,cy2//3),(cx2,cy2//3*2),(0,0,250), 5)
    cv2.rectangle(image,(cx1,cy2//3*2),(cx2,cy2),(0,0,250), 5)
    
    cv2.putText(image, 'COLOR',(cx1+25, int((cy1+cy2)/2)),font, 1, (250,250,250),1, font)
    cv2.putText(image, 'SAVE BITCH',(cx1+30, cy2//6),font, .5, (250,250,250),1, font)
    cv2.putText(image, 'CleAr',(cx1+32,int((cy2//2)+cy2//3)),font, 1, (250,250,250),1, font)

def save(image,current,cx1,cy1,cx2,cy2):
    if cx1 <= current[0] <= cx2:
        if cy1 <= current[1] <= cy2//3:
            return True
def changecolor(image,current,cx1,cy1,cx2,cy2):
    if cx1 <= current[0] <= cx2:
        if cy2//3 <= current[1] <= cy2//3*2:
            return True
def clear(image,current, cx1,cy1,cx2,cy2):
    if cx1 <= current[0] <= cx2:
        if cy2//3*2 <= current[1] <= cy2:
            return True
        
while True:
    width = 1000
    height= 560
    cx1=    int(width-150)
    cy1=    0
    cx2=    width
    cy2=    height
    
    #resizes image
    (b,image) = cam.read()
    image = imutils.resize(image, width=1000)
    image = cv2.flip(image,1)
    #picks HSV color and minimizes noise
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask =cv2.dilate(mask, None, iterations=2)
    mask =cv2.erode(mask, None, iterations=2)
    
    #contours surrounding object
    contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    currentPoint = None
    sideBar(image,cx1,cy1,cx2,cy2)
    #if object detected then create circle
    if len(contour) >= 1:
        #using max contour, find currentPoint point
        c = max(contour, key=cv2.contourArea)
        Mom = cv2.moments(c)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        moment10 = Mom["m10"]
        moment01   = Mom["m01"]
        area = Mom["m00"]
        #prevents division by zero-makes small circle to track color
        if area != 0:
            currentPoint = (int(moment10 / area), int(moment01 /area))
            if currentPoint != None:
                points.append(currentPoint)

        curX, curY = (int(x), int(y))
        rad        = int(radius)
        if radius > 20:
            cv2.circle(image,currentPoint, 5,(0,0,255),-1)
            cv2.circle(image,(curX, curY),rad,(225,255,255),2)
    
    #draws lines on screen
    for pt in range(1, len(points)):
        current= points[pt]
        previous = points[pt-1]
        if previous != None and current != None:
            cv2.line(image, previous, current, (0,250,230), 3)
            
            #checks if cursor is in any of the toolbar features
            if clear(image, current, cx1,cy1,cx2,cy2):
                points = []
            #if color(image,current, cx1,cy1,cx2,cy2):
                #import emotion color detector
            if save(image, current, cx1,cy1,cx2,cy2):
                count+=1
                print("hi")
                cv2.imwrite(os.path.join('C:Users/anburbano/Desktop/term project/', 'image' + str(count)) ,image)

                
    cv2.imshow("image",image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
        
#kill CAMERA
cam.release()
cv2.destroyAllWindows()
        
    
    