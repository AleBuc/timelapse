import logging
from datetime import datetime
from os import system
from time import sleep
from picamera import PiCamera

totalTime = 60  # set the total time of capture in minutes
capturePeriod = 10  # set the period in seconds between 2 taken pictures

numPics = int((totalTime * 60) / capturePeriod)  # number of pictures to take
logging.info(str(numPics) + " pictures to take.")

camera = PiCamera()
camera.resolution = (1920, 1080)

picturesDirectory = '/home/pi/Pictures'

date = datetime.now().isoformat()
picsFolder = picturesDirectory + '/picsTaking' + date
system('mkdir ' + picsFolder)

for i in range(numPics):
    camera.capture(picsFolder + '/img{0:05d}.png'.format(i), format='png')
    sleep(capturePeriod)
logging.info(str(range) + " taken pictures.")
