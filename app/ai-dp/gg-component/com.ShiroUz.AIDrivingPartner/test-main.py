import cv2 as cv
import time
import sys

STDOUT = sys.stdout

sys.stdout = open('./tmp.txt', 'w')

help(sys)
 
sys.stdout = STDOUT

while True:
    print("Checking OpenCV version...")
    print(cv.__version__)
    time.sleep(1)
