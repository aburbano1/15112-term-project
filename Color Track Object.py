import cv2
import numpy as np
import imutils

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

while True:
    #resizes image
    (b,image) = cam.read()
    image = imutils.resize(image, width=1000)
    
    #picks HSV color and minimizes noise
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask =cv2.erode(mask, None, iterations=2)
    
    #contours surrounding object
    contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    currentPoint = None
    
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
    
    for pt in range(1, len(points)):
        current= points[pt]
        previous = points[pt-1]
        if previous != None and current != None:
            cv2.line(image, previous, current, (0,250,230), 3)
    
    image = cv2.flip(image,1)
    cv2.imshow("image",image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("g"):
        break
        
#kill CAMERA
cam.release()
cv2.detroyAllWindows()
        
    
    