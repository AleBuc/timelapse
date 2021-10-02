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
print(str(numPics) + ' pictures to take.')

camera = PiCamera()
camera.resolution = (xResolution, yResolution)

date = datetime.now().isoformat()
if rotation == 0:
    picsToRotateFolder = ''
else:
    picsToRotateFolder = '/to_rotate'

picsFolder = picturesDirectory + '/picsTaking' + date
picsFolderToSave = picsFolder + picsToRotateFolder
os.mkdir(picsFolder)
if rotation != 0:
    os.mkdir(picsFolderToSave)
print('Begin the capture at ' + datetime.now().isoformat() + '.')
for i in range(numPics):
    camera.capture(picsFolderToSave + '/img{0:05d}.png'.format(i), format='png')
    print('Capture ' + str(i) + ' on ' + str(numPics) + '.')
    sleep(capturePeriod)
print(str(range) + ' taken pictures at ' + datetime.now().isoformat() + '.')

if rotation != 0:
    print('Begin to rotate the pictures')
    picsNames = os.listdir(picsFolderToSave)
    for picName in picsNames:
        pic = Image.open(picsFolderToSave + picName)
        pic = pic.rotate(rotation, expand=1)
        pic.save(picsFolder + picName)
        print(picName + ' rotated')
    os.rmdir(picsFolderToSave)
    print('All pics moved in ' + picsFolder)

system('ffmpeg -r {} -f image2 -s '.format(fps) + str(xResolution) + 'x' + str(
    yResolution) + ' -nostats -loglevel 0 -pattern_type glob -i "' + picsFolder + '"/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p ' + videosDirectory + '/{}.mp4'.format(
    date))
