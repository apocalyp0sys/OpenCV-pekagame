# -*- coding: utf-8 -*-

import cv2.cv as cv
import math
import time
import random
import sys


class GObject:
    def __init__(self, sprite, mask):
        self.lived = 0
        self.life = random.randint(5,10)
        self.sprite = sprite
        self.mask = mask
        self.x = 0
        self.y = 0

class Game:
    def __init__(self, color1 = (165,100,150), color2 = (179,255,255)):
        cv.NamedWindow("pekagame", 1)
        self.capture = cv.CaptureFromCAM(0)
        self.color1 = color1
        self.color2 = color2
        self.pekaSprite = cv.LoadImage('res/peka.png', cv.CV_LOAD_IMAGE_COLOR)
        self.pekaMask = cv.LoadImage('res/mask.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
        self.pekaButt = cv.LoadImage('res/butt.png', cv.CV_LOAD_IMAGE_COLOR)
        
        self.Gobjects = []
        self.start = time.clock()
        self.previousSec = 0
        
        self.timeLimit = 60
        self.score = 0
       
    def intersects(self, rect1, rect2):
        a1=int(rect1[0])
        b1=int(rect1[1])
        c1=int(rect1[0]+rect1[2])
        d1=int(rect1[1]+rect1[3])
        a2=int(rect2[0])
        b2=int(rect2[1])
        c2=int(rect2[0]+rect2[2])
        d2=int(rect2[1]+rect2[3])
        
        if(((a1 >= a2 and a1 <= c2) or (c1 >= a2 and c1<= c2)) and ((b1 >= b2 and b1 <= d2) or (d1 >= b2 and d1 <= d2))):
            return True
        else:
            return False
            
    
    """ 
    def intersects(self, al, be, img=0):
        a = al[0]
        b = al[1]
        c = al[0] + al[2]
        d = al[1] + al[3]
        e = be[0]
        f = be[1]
        g = be[0] + be[2]
        h = be[1] + be[3]      
        
        if(((a >= e and a<= g) or (c >= e and c <= g)) and ((b >= f and b <= h) or (d >= f and d <= h))):
            return True
        else:
            return False
        """
            
    def drawObj(self, img, gobj):
        cv.SetImageROI(img, (gobj.x, gobj.y, gobj.sprite.width, gobj.sprite.height))
        cv.Copy(gobj.sprite, img, self.pekaMask)
        cv.ResetImageROI(img)
        
    def run(self):
        while True:
            sec = math.floor(time.clock())
            img = cv.QueryFrame(self.capture)
            cv.Flip(img,img,1)  
            
            imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3)
            cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV)
     
            imgBG = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.InRangeS(imgHSV,self.color1,self.color2,imgBG)
            #cv.Smooth(imgBG, imgBG, cv.CV_MEDIAN, 7)

            moments = cv.Moments(cv.GetMat(imgBG))
    
            m10 = cv.GetSpatialMoment(moments, 1, 0)
            m01 = cv.GetSpatialMoment(moments, 0, 1)
            m00 = cv.GetCentralMoment(moments, 0, 0)
    
            if(m00 > 0):    
                posX = int(m10/m00)
                posY = int(m01/m00)
                 
                #print posX, posY
                
            dim = cv.CreateImage((640,480),8,3)
            cv.SetZero(dim)
            cv.AddWeighted(dim, 1.0, img, 0.3, 0, img)
            
            if(sec - self.previousSec == 1):
                
                for i in self.Gobjects:
                    i.lived += 1
                    if(i.lived >= i.life):
                        self.Gobjects.remove(i)
                
                if(len(self.Gobjects) < 25):
                    for z in [1,2]:
                        peka = GObject(self.pekaSprite, self.pekaMask)
                        peka.x = random.randint(0, 640 - peka.sprite.width)
                        peka.y = random.randint(0, 480 - peka.sprite.height)
                        
                        intersect  = False                    
                        for i in self.Gobjects:
                            if(self.intersects((peka.x, peka.y, peka.sprite.width,peka.sprite.height),
                                               (i.x, i.y, i.sprite.width,i.sprite.height))):
                                intersect = True
                                
                        
                        #print intersect
                        if(not intersect):
                            self.Gobjects.append(peka)
                        
                    #print len(self.Gobjects)        
            
            for i in self.Gobjects:
                if(m00 > 0  and self.intersects((i.x, i.y, i.sprite.width,i.sprite.height),(posX-15,posY-15,30,30))
                    and i.sprite != self.pekaButt):
                    i.sprite = self.pekaButt
                    self.score += 10 + (10 - i.lived)
                    i.life = 1
                    i.lived = 0     
                self.drawObj(img,i)
             
            if(m00 > 0): 
                pass
                cv.Circle(img, (posX, posY), 5, (0,0,255), 5, cv.CV_AA)
                cv.Rectangle(img, (posX-15, posY-15), (posX+15, posY+15), (0,0,255), 1) 
            
            font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX, 0.5, 0.5, 0.1, 1, cv.CV_AA)
            cv.PutText(img, 'Score: ' + str(self.score), (0, 13), font, (150, 150,200))
            cv.PutText(img, 'Time: ' + str(self.timeLimit - int(sec)), (563, 13), font, (150, 150,200))            
          
            cv.ShowImage("pekagame",img)
            
            self.previousSec = sec            
            
            if(sec >= self.timeLimit):
                cv.PutText(img, 'GAME OVER', (260, 150), font, (50, 150,50))
                cv.ShowImage("pekagame", img)
                cv.WaitKey(0)
                break
           
            if cv.WaitKey(20) == 27:
                break
    
    
if __name__=="__main__":
    print "Press Esc to exit"
    print "Hunt Peka-faces with reddish objects! Make 'em butthurt!"
    args = sys.argv
    if(len(args) == 7):
        game = Game((int(args[1]),int(args[2]),int(args[3])),(int(args[4]),int(args[5]),int(args[6])))
    else:
        game = Game()    
    game.run()
    cv.DestroyAllWindows()