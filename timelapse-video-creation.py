import os
from datetime import datetime
from os import system
from time import sleep

from PIL import Image
from picamera import PiCamera

totalTime = 120  # set the total time of capture in minutes
capturePeriod = 4  # set the period in seconds between 2 taken pictures
rotation = 180  # set the angle of rotation needed for the pictures.
fps = 60  # set number of frames per second of the video
xResolution = 1024
yResolution = 768
picturesDirectory = '/home/pi/Pictures'
videosDirectory = '/home/pi/Videos'

numPics = int((totalTime * 60) / capturePeriod)  # number of pictures to take

date = datetime.now().isoformat()
if rotation == 0:
    picsToRotateFolder = ''
else:
    picsToRotateFolder = '/to_rotate'

picsFolder = picturesDirectory + '/picsTaking' + date
picsFolderToSave = picsFolder + picsToRotateFolder

system('ffmpeg -r {} -f image2 -s '.format(fps) + str(xResolution) + 'x' + str(
    yResolution) + ' -nostats -loglevel 0 -pattern_type glob -i "' + picsFolder + '"/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p ' + videosDirectory + '/{}.mp4'.format(
    date))
