import cv2
import numpy as np
import imutils

### Basic FRAME

cam = cv2.VideoCapture(0)
start = True

def startScreen(image):
    width = 1000
    height = 800
    cx1=    int(width/4)
    cy1=    int(height/3)
    cx2=    int(width/3*2)
    cy2=    int(height/4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, 'Drawing With Emotion',(cx1-50, int((cy1+cy2)/2)),font, 2, (250,250,250),2, cv2.LINE_AA)
    cv2.putText(image, 'Press "s" to Start cutie',(cx1+60, cy1+50),font, 1,   (250,250,250),2, cv2.LINE_AA)
    
while True:
    #resizes and flips image
    (b,image) = cam.read()
    image = imutils.resize(image, width=1000)
    image = cv2.flip(image,1)
    if start==True:
        startScreen(image)
    cv2.imshow("image",image)
    if start==False:
        import colorTrackObject.py         
    
    #KeyPress controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        start = False
    if key == ord("q"):
        break
    

   
        
    
cam.release()
cv2.destroyAllWindows()