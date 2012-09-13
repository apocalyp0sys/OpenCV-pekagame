# -*- coding: utf-8 -*-

import cv2.cv as cv

capture = cv.CaptureFromCAM(0)
cv.NamedWindow("test",1)
cv.NamedWindow("test2",1)

while True:
    img = cv.QueryFrame(capture)
    
    imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
     
    imgBG = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.InRangeS(imgHSV,(165,100,150),(179,255,255),imgBG)
    #imgBG1 = cv.CreateImage(cv.GetSize(img), 8, 1)
    #cv.InRangeS(imgHSV,(0,100,150),(10,255,255),imgBG1)
    #imgBG2 = cv.CreateImage(cv.GetSize(img), 8, 1)
    #cv.InRangeS(imgHSV,(160,150,150),(179,255,255),imgBG2)
    
    #cv.Copy(imgBG1, imgBG2)
    
    moments = cv.Moments(cv.GetMat(imgBG))
    
    m10 = cv.GetSpatialMoment(moments, 1, 0)
    m01 = cv.GetSpatialMoment(moments, 0, 1)
    m00 = cv.GetCentralMoment(moments, 0, 0)
    
    if(m00 > 0):    
        posX = m10/m00
        posY = m01/m00
    
        #print posX, posY
        
        cv.Circle(img, (int(posX), int(posY)), 5, (255,0,0), 5, cv.CV_AA)
    
    cv.ShowImage("test", img)
    cv.ShowImage("test2", imgBG)
    
    if(cv.WaitKey(20)!= -1):
        break