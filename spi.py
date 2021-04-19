import cv2
import numpy as np
import spidev
from time import sleep

# spi master mode configuration
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 125000000

#function send a character to MSP430
def write_pot(input):
    msb = input >> 8
    lsb = input & 0xFF
    spi.xfer([msb,lsb])

#Open the camera
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    sleep(0.025)    #delay
    ret,frame =cap.read()   #get a frame from the video
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  #Gray conversion 
    retval,dst = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)  #image thresholding
    dst = cv2.dilate(dst,None,iterations=2) #dilate the white area
    dst = cv2.erode(dst,None,iterations=2)  #erode the white area
    cv2.imshow("dst",dst)   #show the processed video
    color = dst[460]    #choose the line with hight = 460 
    
    #Direction controle
    try:
        white_count=np.sum(color == 255)    #sum of the number of white pixel
        white_index=np.where(color==255)    #position of all the white pixel
        if white_count == 0:    #avoid the error
            white_count = 1
        center = (white_index[0][white_count-1]+white_index[0][0]) / 2      #calculer the centre of the white line
        
        #Compare the centre of the white line and the camera , and respond accordingly
        if center < 270:
            write_pot(0x32)     #0x32 --> turn left
            print(center)
        elif center > 330:
            write_pot(0x31)     #0x31 --> turn right
            print(center)
        else:
            write_pot(0x33)     #0x33 --> go straight
            print(center)
    except:
        pass
    if cv2.waitKey(1)&0xFF == ord('q'):     #press 'q' to exit
        break
cap.release()
cv2.destroyAllWindows()
