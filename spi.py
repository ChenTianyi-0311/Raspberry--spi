import cv2
import numpy as np
import spidev
from time import sleep


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 125000000

def write_pot(input):
    msb = input >> 8
    lsb = input & 0xFF
    spi.xfer([msb,lsb])

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    sleep(0.025)  
    ret,frame =cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    retval,dst = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)
    dst = cv2.dilate(dst,None,iterations=2)
    dst = cv2.erode(dst,None,iterations=2)
    cv2.imshow("dst",dst)
    color = dst[460]
    try:
        white_count=np.sum(color == 255)
        white_index=np.where(color==255)
        if white_count == 0:
            white_count = 1
        center = (white_index[0][white_count-1]+white_index[0][0]) / 2
        if center < 270:
            write_pot(0x32)
            print(center)
        elif center > 330:
            write_pot(0x31)
            print(center)
        else:
            write_pot(0x33)
            print(center)
    except:
        pass
    if cv2.waitKey(1)&0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
