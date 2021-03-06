from __future__ import division
import dlib
import cv2
import numpy as np
import imutils
neutral = False
draw = False
open = False
erase = False
thickyy = False

##code credit to  oarriaga on github
def resize(img, width=None, height=None, interpolation=cv2.INTER_AREA):
    global ratio
    w, h = img.shape
    if width is None and height is None:
        return img
    elif width is None:
        ratio = height / h
        width = int(w * ratio)
        resized = cv2.resize(img, (height, width), interpolation)
        return resized
    else:
        ratio = width / w
        height = int(h * ratio)
        resized = cv2.resize(img, (height, width), interpolation)
        return resized
        
def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords
camera = cv2.VideoCapture(0)
predictor_path = '../shape_predictor_68_face_landmarks.dat_2'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
####
#following code tracks a certain color (spanish orange)
    #then finds coordinates of largest contours
        #then uses these coordinates to create a circle around object 
            #uses coordinates to draw line segment from current pnt to previous
###

lower = np.array([7,150,180])
upper = np.array([100,250,250])
points = []
cam = cv2.VideoCapture(0)
count =0
def sideBar(image,cx1,cy1,cx2,cy2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    cv2.rectangle(image,(cx1,cy1),(cx2,cy2//3-4),(0,0,250), 5) 
     
    cv2.rectangle(image,(cx1,cy2//3+1),(cx2-3,cy2//5*2+30),(0,250,250), 2)
    cv2.rectangle(image,(cx1,cy2//5*2+30),(cx2-3,cy2//4*2+30),(0,250,250), 2)
    cv2.rectangle(image,(cx1,cy2//4*2+30),(cx2-3,cy2//3*2-3),(0,250,250), 2)
    
    cv2.rectangle(image,(cx1,cy2//3*2+2),(cx2-3,cy2),(0,0,250), 5)
    
    
    cv2.putText(image, 'THICKY',(cx1+15, int((cy1+cy2)/3+44)),font, 1.2, (250,250,250),4, font)
    cv2.putText(image, 'medium',(cx1+23, int((cy1 + cy2)/2+9)),font, .7, (250,250,250),2, font)
    cv2.putText(image, 'thin',(cx1+45, int((cy1+cy2)/3*2-30)),font, .5, (250,250,250),1, font)
    
    
    cv2.putText(image, 'SAVE BITCH',(cx1+30, cy2//6),font, .5, (250,250,250),1, font)
    cv2.putText(image, 'CleAr',(cx1+32,int((cy2//2)+cy2//3)),font, 1, (250,250,250),1, font)

def save(image,current,cx1,cy1,cx2,cy2):
    if cx1 <= current[0] <= cx2:
        if cy1 <= current[1] <= cy2//3:
            return True
            
def thicky(image,current,cx1,cy1,cx2,cy2):
    if cx1 <= current[0] <= cx2:
        if cy2//3+1 <= current[1] <= cy2//5*2+30:
            return True
def medium(image,current,cx1,cy1,cx2,cy2):
    if cx1 <= current[0] <= cx2:
        if cy2//5*2+30 <= current[1] <= cy2//4*2+30:
            return True
def thin(image,current,cx1,cy1,cx2,cy2):
    if cx1 <= current[0] <= cx2:
        if cy2//4*2+30 <= current[1] <= cy2//3*2-3:
            return True
            
# def erase(image,current,cx1,cy1,cx2,cy2):
#     if cx1 <= current[0] <= cx2:
#         if cy2//3 <= current[1] <= cy2//3*2:
#             return True
# 
def clear(image,current, cx1,cy1,cx2,cy2):
    if cx1 <= current[0] <= cx2:
        if cy2//3*2 <= current[1] <= cy2:
            return True
        
###expressions CUtie
def openMouth(ratio, shape, callibrations):
    x1,y1 =  shape[61][0], shape[61][1]
    x2,y2 =  shape[67][0], shape[67][1]
    
    x3,y3 =  shape[62][0], shape[62][1]
    x4,y4 =  shape[66][0],shape[66][1]
    
    x5,y5 =  shape[63][0],shape[63][1]
    x6,y6 =  shape[65][0], shape[65][1]
    
    if (((y6-y5)**2 +(x6-x5)**2)**.5 + ((y4-y3)**2 +(x4-x3)**2)**.5 + ((y2-y1)**2 +(x2-x1)**2)**.5) < 7 :
        return False
    else: return True

def angry(ratio, shape, callibrations):
    #angered expression -eyebrows 
    x1,y1 = shape[19][0], shape[19][1]
    x2,y2 = shape[24][0], shape[24][1]
    x3,y3 = shape[20][0], shape[20][1]
    x4,y4 = shape[23][0], shape[23][1]
    x5,y5 = shape[21][0], shape[21][1]
    x6,y6 = shape[22][0], shape[22][1]
    
    #neutral face
    a1,b1 = callibrations[19][0],callibrations[19][1]
    a2 ,b2 = callibrations[24][0],callibrations[24][1]
    a3,b3 = callibrations[20][0], callibrations[20][1]
    a4,b4 = callibrations[23][0], callibrations[23][1]
    a5,b5 = callibrations[21][0], callibrations[21][1]
    a6,b6 = callibrations[22][0], callibrations[22][1]
    
    #distance between nose and lower part of upper lip 
    c1, d1 = shape[32][0],shape[32][1]
    c2,d2 = shape[61][0] ,shape[61][1]
    c3, d3 = shape[33][0],shape[33][1]
    c4, d4 = shape[62][0],shape[62][1]
    c5,d5 = shape[34][0], shape[34][1]
    c6,d6 = shape[63][0], shape[63][1]
    c7,d7 = callibrations[32][0], callibrations[32][1]
    c8,d8 = callibrations[61][0] ,callibrations[61][1]
    c9,d9 = callibrations[33][0],callibrations[33][1]
    c10,d10 = callibrations[62][0], callibrations[62][1]
    c11,d11 = callibrations[34][0], callibrations[34][1]
    c12,d12 = callibrations[63][0], callibrations[63][1]
    
    #scrunched up face
    scrunched = (((d6-d5)**2 +(c6-c5)**2)**.5 + ((d4-d3)**2 +(c4-c3)**2)**.5 + ((d2-d1)**2 +(c2-c1)**2)**.5 )
    neut =(((d12-d11)**2 +(c12-c11)**2)**.5 + ((d10-d9)**2 +(c10-c9)**2)**.5 + ((d8-d7)**2 +(c8-c7)**2)**.5 )
    #lateral distances betwen points on eyebrows-ANGRY EYEBROWS VS NEUTRAL
    cali=(((b6-b5)**2 +(a6-a5)**2)**.5 + ((b4-b3)**2 +(a4-a3)**2)**.5 + ((b2-b1)**2 +(a2-a1)**2)**.5) 
    sha =(((y6-y5)**2 +(x6-x5)**2)**.5 + ((y4-y3)**2 +(x4-x3)**2)**.5 + ((y2-y1)**2 +(x2-x1)**2)**.5 )
    if cali > sha:
        if openMouth(ratio, shape, callibrations):
            if scrunched < neut:
                return True
    else: return False

def happy(ratio, shape, callibrations):
    #points on lips
    x1,y1 = shape[48][0], shape[48][1]
    x2,y2 = shape[59][0], shape[59][1]
    x3,y3 = shape[58][0], shape[58][1]
    x4,y4 = shape[56][0], shape[56][1]
    x5,y5 = shape[55][0], shape[55][1]
    x6,y6 = shape[54][0], shape[54][1]
    a1,b1 = callibrations[48][0], callibrations[48][1]
    a2,b2 = callibrations[54][0], callibrations[54][1]
    a7,b7 = callibrations[59][0], callibrations[59][1]
    a8,b8 = callibrations[58][0], callibrations[58][1]
    #points on eyes
    x7,y7 = shape[41][0], shape[41][1]
    x8,y8 = shape[37][0], shape[37][1]
    x9,y9 = shape[38][0], shape[38][1]
    x10,y10 =shape[40][0], shape[40][1]
    a3,b3 = callibrations[41][0],callibrations[41][1]
    a4,b4 = callibrations[46][0],callibrations[46][1]
    a5,b5 = callibrations[37][0],callibrations[37][1]
    a6,b6 = callibrations[44][0], callibrations[44][1]
    x11,y11 = shape[43][0], shape[43][1]
    x12,y12 = shape[47][0], shape[47][1]
    x13,y13 = shape[46][0], shape[46][1]
    x14,y14 = shape[44][0], shape[44][1]
    
    #distance between points on lips, should be larger than 26 if smiling
    happylip=(((y2-y1)**2 +(x2-x1)**2)**.5 + ((y3-y2)**2 +(x3-x2)**2)**.5) 
    neutlip=(((b7-b1)**2 +(a7-a1)**2)**.5 + ((b7-b8)**2 +(a7-a8)**2)**.5) 
    #distance between farthest points on edge of lips
    happy=((y6-y1)**2 +(x6-x1)**2)**.5
    neut=((b2-b1)**2 +(a2-a1)**2)**.5
    #distnace between lip and eyes
    neutEL= ((b1-b3)**2 +(a1-a3)**2)**.5 + ((b2-b4)**2 +(a2-a4)**2)**.5
    happyEL= ((y7-y1)**2 +(x7-x1)**2)**.5 + ((y13-y6)**2 +(x13-x6)**2)**.5
    #distance between eyes
    neuteyes= ((b5-b3)**2 +(a5-a3)**2)**.5 + ((b6-b4)**2 +(a6-a4)**2)**.5
    happyeyes= ((y7-y8)**2 +(x7-x8)**2)**.5 + ((y13-y14)**2 +(x13-x14)**2)**.5
    
    if happylip > neutlip:
        if happy/neut >= 1.2:
           if openMouth(ratio, shape, callibrations):
               if neutEL / happyEL >=1.1:
                    if happyeyes < neuteyes:
                        return True
    else: return False
    
def shocked(shape, callibrations):
    #points on eyes
    x1,y1 = shape[44][0], shape[44][1]
    x2,y2 = shape[46][0], shape[46][1]
    x3,y3 = shape[43][0], shape[43][1]
    x4,y4 = shape[47][0], shape[47][1]
    #eyebrow
    x5,y5 = shape[25][0], shape[25][1]
    #nose to chin comparison
    x6,y6 = shape[27][0], shape[27][1]
    x7,y7 = shape[7][0],  shape[7][1]
    
    #points on eyes-neutral
    a1,b1 = callibrations[44][0], callibrations[44][1]
    a2,b2 = callibrations[46][0], callibrations[46][1]
    a3,b3 = callibrations[43][0], callibrations[43][1]
    a4,b4 = callibrations[47][0], callibrations[47][1]
    #eyebrow-neutral
    a5,b5 = callibrations[25][0], callibrations[25][1]
    #nose to chin comparison-neutral
    a6,b6 = callibrations[27][0], callibrations[27][1]
    a7,b7 = callibrations[7][0],  callibrations[7][1]
    
    #compares distance btw BIG open Eyes and chill neutral EYEs
    shockeye= (((y2-y1)**2+(x2-x1)**2)**.5+((y3-y4)**2+(x3-x4)**2)**.5) 
    neuteyes= (((b2-b1)**2+(a2-a1)**2)**.5 + ((b3-b4)**2+(a3-a4)**2)**.5)
    #compares distance btw SHOCKED HIGH EYEBROWS and chIll eyebrows
    Nbrow= (((b5-b1)**2+(a5-a1)**2)**.5)  
    Sbrow= (((y5-y1)**2+(x5-x1)**2)**.5) 
    #comparison between pt on nose and chin
    Nchin= (((b7-b6)**2+(a7-a6)**2)**.5)  
    Schin= (((y7-y6)**2+(x7-x6)**2)**.5)
     
    if shockeye / neuteyes >= 1.2:
       if Sbrow / Nbrow >= 1.1:
           if openMouth(ratio, shape, callibrations):
                if Schin/ Nchin >= 1.1:
                  return True
    else: return False
    
###code for changing THICKNESSSFSFSFS of line
def right(shape, callibrations):
    x1,y1 = shape[12][0], shape[12][1]
    x2,y2 = shape[54][0], shape[54][1]
    x3,y3 = shape[48][0], shape[48][1]
    x4,y4 = shape[5][0],  shape[5][1]
    x5,y5 = shape[36][0],  shape[36][1]
    
    a1,b1 = callibrations[12][0], callibrations[12][1]
    a2,b2 = callibrations[54][0], callibrations[54][1]
    a3,b3 = callibrations[48][0], callibrations[48][1]
    a4,b4 = callibrations[5][0],  callibrations[5][1]
    a5,b5 = callibrations[36][0],  callibrations[36][1]
    mouthS = (((y2-y1)**2+(x2-x1)**2)**.5 + ((y3-y2)**2+(x3-x2)**2)**.5) 
    mouthN = (((b2-b1)**2+(a2-a1)**2)**.5 + ((b3-b2)**2+(a3-a2)**2)**.5) 
    MS = ((y4-y3)**2+(x4-x3)**2)**.5
    MN = ((b4-b3)**2+(a4-a3)**2)**.5
    if mouthN / mouthS > 1.08:
       if MS / MN > 1.4:
           return True
    else: return False

def left(shape, callibrations):
    x1,y1 = shape[12][0], shape[12][1]
    x2,y2 = shape[54][0], shape[54][1]
    x3,y3 = shape[48][0], shape[48][1]
    x4,y4 = shape[5][0],  shape[5][1]
    x5,y5 = shape[36][0],  shape[36][1]
    
    a1,b1 = callibrations[12][0], callibrations[12][1]
    a2,b2 = callibrations[54][0], callibrations[54][1]
    a3,b3 = callibrations[48][0], callibrations[48][1]
    a4,b4 = callibrations[5][0],  callibrations[5][1]
    a5,b5 = callibrations[36][0],  callibrations[36][1]
    mouthS = (((y2-y1)**2+(x2-x1)**2)**.5 + ((y3-y2)**2+(x3-x2)**2)**.5) 
    mouthN = (((b2-b1)**2+(a2-a1)**2)**.5 + ((b3-b2)**2+(a3-a2)**2)**.5) 
    MS = ((y4-y3)**2+(x4-x3)**2)**.5
    MN = ((b4-b3)**2+(a4-a3)**2)**.5
    if mouthS / mouthN > 1.08:
       if MN / MS > 1.4:
           return True
    else: return False
    
    
    
while True:
    width = 1000
    height= 560
    cx1=    int(width-150)
    cy1=    0
    cx2=    width
    cy2=    height
    (ret, frame) = camera.read()
    frame = imutils.resize(frame, width=1000)                    
    frame = cv2.flip(frame,1)
    
#drawing template
    background = np.ones((168,300,3), np.uint8)
    back = imutils.resize(background, width=1000)                    
    back = cv2.flip(back,1)

    
    
    
    
    ###code for DRAWING THE LINEE
    #picks HSV color and minimizes noise
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask =cv2.dilate(mask, None, iterations=2)
    mask =cv2.erode(mask, None, iterations=2)
    
    #contours surrounding object
    contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    currentPoint = None
    sideBar(frame,cx1,cy1,cx2,cy2)
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
            if draw != True:
                currentPoint = None
            else: currentPoint = (int(moment10 / area), int(moment01 /area))
            points.append((currentPoint, color, thickness))
        curX, curY = (int(x), int(y))
        rad        = int(radius)
        if radius > 20:
            cv2.circle(frame,currentPoint, 5,(0,250,230),-1)
            cv2.circle(frame,(curX, curY),rad,(225,255,255),2)
    ###code for, like, changing facial expressions
    if ret == False:
        print('Failed to capture frame from camera')
        break
    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_resized = resize(frame_grey, 120)
    dets = detector(frame_resized, 1)
    lmao = 0
    if len(dets) > 0:
        for k, d in enumerate(dets):
            #(x,y)
            shape = predictor(frame_resized, d)
            shape = shape_to_np(shape)
            for (x, y) in shape:
                lmao +=1
                #my code
                #checks facial expression 
                if neutral == True:
                    open = True
                    callibrations = shape
                    cv2.circle(frame,(int(x/ratio),int(y/ratio)),1,(205,0,255),-1) 
                if open == True:                
                    font = cv2.FONT_HERSHEY_SIMPLEX 
                    if happy(ratio, shape, callibrations) == True:
                        cv2.putText(frame, "Oh SHEs HappY YAY", (500, 500), font, 1, (250,250,250), 2, cv2.LINE_AA)
                        color = (0,250,230)
                    elif angry(ratio, shape, callibrations) == True:
                        cv2.putText(frame, "GR ANGRY! >:(", (500, 500), font, 1, (250,250,250), 2, cv2.LINE_AA)
                        color = (0,0,250)
                    elif shocked(shape, callibrations) == True:
                        cv2.putText(frame, "ShOcked lil boy :o", (500, 500), font, 1, (250,250,250), 2, cv2.LINE_AA)
                        color = (0,200,250)
                    elif right(shape, callibrations):
                        thickyy = True
                        cv2.putText(frame, "THICKKKK", (500, 500), font, 1, (250,250,250), 2, cv2.LINE_AA)
                        if thickness < 20:
                            if lmao % 25 ==0:
                                thickness +=1
                    elif left(shape, callibrations):
                        thickyy = True
                        cv2.putText(frame, "thin baby", (500, 500), font, 1, (250,250,250), 2, cv2.LINE_AA)
                        if thickness >1:
                            if lmao % 25 ==0:
                                thickness -=1
                else: color = (0,250,0)
                #checks position of mouth 

    if thickyy == False:
        thickness = 8
                
                
            
    #draws lines on screen
    for pt in range(1, len(points)):
        current= points[pt][0]
        previous  = points[pt-1][0]
        colors    = points[pt-1][1]
        thicknesss = points[pt-1][2]

        if previous != None and current != None :
            cv2.line(frame, previous, current, colors, thicknesss)
            cv2.line(back, previous, current, colors, thicknesss)
            #checks if cursor is in any of the toolbar features
            if clear(frame,current,cx1,cy1,cx2,cy2):
                points = []
            if save(frame, current, cx1, cy1, cx2, cy2):
                count+=1
    
            if thicky(frame,current,cx1,cy1,cx2,cy2):
                thickyy = True
                thickness = 15
            if medium(frame,current,cx1,cy1,cx2,cy2):
                thickness = 8
            if thin(frame,current,cx1,cy1,cx2,cy2):
                thickyy = True
                thickness = 1

    
    
    
    
    cv2.imshow("drawing cutie", back)
    cv2.imshow("image", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()
        camera.release()
        break
    #callibrates a neutral face 
    if key == ord('c'):
        neutral = True
    if key == ord('v'):
        neutral = False
    #controls draw function
    if key== ord('d'):
        draw = True
    if key == ord('f'):
        draw = False
    #controls erase function
    if key ==ord('e'):
        erase = True
    if key == ord('r'):
        erase = False
    #controls line thickness function
    if key ==ord('t'):
        thickyy = True
    if key == ord('y'):
        thickyy = False