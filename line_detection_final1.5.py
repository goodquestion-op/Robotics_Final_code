# You may run into issues installing pytesseract, this is because python wants you to install things into virtual environments
# For our usecase, venv aren't super useful as we are only making one project at a time, so use the flags below:
# sudo pip3 install pytesseract --break-system-packages
# https://nanonets.com/blog/ocr-with-tesseract/
from PIL import Image
#import pytesseract
import cv2
import os, sys, inspect #For dynamic filepaths
import numpy as np;
import serial
import time
import math
import itertools



hough_count = 0
Cx = 0
Cy = 0
m = 0

cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam.set(cv2.CAP_PROP_FPS, 30)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()


while True:
    
    check, frame = cam.read()

    image = cv2.resize(frame,(320,240))
    # Resize

     # Greyscale
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #blur
    #blur = cv2.GaussianBlur(grey,(11,11),3)
    blur = cv2.blur(grey,(5,5))

   
    

    # Threshold         120 is threshold, 255 is what we assign if it is below this
    _, thresh = cv2.threshold(image, 90, 255, cv2.THRESH_BINARY)

    # Canny
    #image = cv2.Canny(image, 50,200,)
    


    # #hough lines
    dst = cv2.Canny(blur, 50, 200, None,3)

    cdst = cv2.cvtColor(dst,cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    list = []
    
    lines = cv2.HoughLines(dst,1,np.pi/180,150,None,0,20)
    if lines is not None:
        for i in range(0,len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)),int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)),int(y0 - 1000*(a)))

            cv2.line(cdst, pt1 ,pt2, (255,0,0), 3, cv2.LINE_AA)
            print(pt1,pt2)

    linesP = cv2.HoughLinesP(dst,1,np.pi/180,50,None,90,90)

    if linesP is not None:
        for i in range(1,len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0],l[1]),(l[2],l[3]),(255,0,255),3,cv2.LINE_AA)
            
            hough_count = i
            Cx = int((l[2]+l[0])/2)
            Cy = int((l[3]+l[1])/2)
            if ((l[2]-l[0])==0):
                m=(0)
            elif (l[3]-l[1] != 0): 
                m = int(((l[3]-l[1])/(l[2]-l[0]))*1000)
            else:
                print("nope")

        #    print(Cx, Cy,m)
         #   print("(",l[0],",",l[1],")","(",l[2],",",l[3],")")
           # cv2.circle(cdstP, (Cx,Cy), 20 ,(0,255,0),4)
            list.insert(1, m)
            
    else:
        hough_count = 0
  #  print(hough_count)        
  #  print(list)

    for a, b in itertools.combinations(list, 2):
        para = (abs(a) - abs(b))
      #  print(para)
        if -80 < para < 80 :
            # print("parallel")
            # print(a)
            # print(b)
            # print("found")
            
            # cv2.line(cdstP,(0,240),(640,240),(255,105,200),3)

            # cv2.line(cdstP,(150,480),(150,0),(255,255,200),3)

            # cv2.line(cdstP,(500,480),(500,0),(255,255,200),3)
            if ( a and b != 0):
                ax1 = int(((480 - 240)/(a/1000))+150)
                ax2 = int(((-240)/(a/1000))+150)
                bx1 = int(((480 - 240)/(b/1000))+500)
                bx2 = int(((-240)/(b/1000))+500)
                # cv2.line(cdstP,(ax1,480),(ax2,0),(255,255,200),3)
                # cv2.line(cdstP,(bx1,480),(bx2,0),(255,255,200),3)
                cx1 = int((bx1+ax1)/2)
                cx2 = int((bx2+ax2)/2)

                cv2.line(cdstP,(cx1,480),(cx2,0),(255,255,200),3)
                cv2.line(cdstP,(320,480),(320,0),(0,255,200),3)
                ending = "\n"
                AD = str(str(cx1)+ending)
                print((AD))
                ser.write((AD).encode('utf-8'))

                if ser.in_waiting > 0:
            
                    # Decode and write it out to console
                    line = ser.readline().decode('utf-8').rstrip()
           
                    print(line)
            # else:
            #     cv2.line(cdstP,(150,480),(150,0),(255,255,200),3)

            #     cv2.line(cdstP,(500,480),(500,0),(255,255,200),3)



    
    print("-------------------------------------------------------------------------------")

    # cdstPg = cv2.cvtColor(cdstP, cv2.COLOR_BGR2GRAY)
    # _, cdstPBI = cv2.threshold(cdstPg, 70, 255, cv2.THRESH_BINARY)
    
    #line = cv2.line(cdstP,(0,240),(640,240),(255,105,100),3)
    PH = cdstP
    
    
    cv2.imshow("Detected Lines (in red) - probabilistic Line Transform", PH)

    cv2.imwrite("image_box_text.jpg",PH)

    key = cv2.waitKey(1)
    if key == 27:
        break
      


cam.release()
cv2.destroyAllWindows()


# Countours (needs canny)
#contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#print("Number of Contours Found = " + str(len(contours)))
#image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#cv2.drawContours(image, contours, -1, (255,0,0),2) #

