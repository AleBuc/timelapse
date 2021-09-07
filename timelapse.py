import logging
from time import sleep
from picamera import PiCamera

totalTime = 60  # set the total time of capture in minutes
capturePeriod = 10  # set the period in seconds between 2 taken pictures

numPics = int((totalTime * 60) / capturePeriod)  # number of pictures to take
logging.info(str(numPics) + " pictures to take.")

camera = PiCamera()
camera.resolution = (1920, 1080)

for i in range(numPics):
    camera.capture('/home/pi/Pictures/image'+str(i)+'.jpg')
    sleep(capturePeriod)
logging.info(str(range) + " taken pictures.")
