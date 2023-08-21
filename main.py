import cv2
import HandTrackingModule as htm
import numpy as np
# import mediapipe as mp

cap = cv2.VideoCapture(0)

detector = htm.handDetector()

draw_color=(255,255,50)

img_canvas = np.zeros((720,1280,3),np.uint8)


while True:
    sucess,frame = cap.read()
    img = cv2.resize(frame,(1280,720))
    cv2.rectangle(img,(0,50),(150,150),(0,0,255),-5)
    cv2.rectangle(img,(155,50),(305,150),(0,100,0),-5)
    cv2.rectangle(img,(310,50),(455,150),(255,48,48),-5)
    cv2.rectangle(img,(460,50),(605,150),(100,255,0),-5)
    cv2.rectangle(img,(610,50),(755,150),(255,255,50),-5)
    cv2.putText(img,text='Eraser',org=(6,110),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=0.75, color=(0,0,0), thickness=2)
    
    #find hands
    img = detector.findHands(img)
    lmlist=detector.findPosition(img)
    # print(lmlist)
    

    if len(lmlist)>0:
       x1,y1=lmlist[8][1:]
       x2,y2=lmlist[12][1:]
    #    print(x1,y1)

    #check fingers up
       
       fingers=detector.fingersUp()
    #    print(fingers)

    #    x3=fingers[1:3]
    #    print(x3)
    #selection mode - index and middle finger up
       if fingers[1] and fingers[2]:
        #    print('selection mode')
           xp,yp=0,0

           if y1<150:
               if 0<x1<150:
                #    print('red')
                   draw_color=(0,0,0)
               elif 155<x1<305:
                   print('green')
                   draw_color=(0,100,0)
               elif 310<x1<455:
                   print('blue')
                   draw_color=(255,48,48)
               elif 460<x1<605:
                   print('yellow')
                   draw_color=(100,255,0)
               elif 610<x1<755:
                   print('sky')
                   draw_color=(255,255,50)

           cv2.rectangle(img,(x1,y1),(x2,y2),draw_color,-1)
               
    # drawing mode
       if fingers[1] and not fingers[2]:
           print('drawing mode')

           if xp == 0 and yp == 0:
               xp = x1
               yp = y1

           if draw_color == (0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),draw_color,50)
                cv2.line(img_canvas,(xp,yp),(x1,y1),draw_color,50)
           else:
               cv2.line(img,(xp,yp),(x1,y1),draw_color,10)
               cv2.line(img_canvas,(xp,yp),(x1,y1),draw_color,10)

               
            
           xp,yp = x1,y1

    
    img_gray = cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)
    _,img_inverse = cv2.threshold(img_gray,20,255,cv2.THRESH_BINARY_INV)
    img_inverse = cv2.cvtColor(img_inverse,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,img_inverse)
    img = cv2.bitwise_or(img,img_canvas)


    img = cv2.addWeighted(img,1,img_canvas,0.5,0)
  
    cv2.imshow('hand_tracking',img)
    # cv2.imshow('canvas',img_canvas)
    

    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
