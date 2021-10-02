import os
from datetime import datetime

from PIL import Image

totalTime = 120  # set the total time of capture in minutes
capturePeriod = 4  # set the period in seconds between 2 taken pictures
rotation = 180  # set the angle of rotation needed for the pictures.
fps = 60  # set number of frames per second of the video
xResolution = 1024
yResolution = 768
picturesDirectory = '/home/pi/Pictures'
videosDirectory = '/home/pi/Videos'

date = datetime.now().isoformat()
if rotation == 0:
    picsToRotateFolder = ''
else:
    picsToRotateFolder = '/to_rotate'

picsFolder = picturesDirectory + '/picsTaking' + date
picsFolderToSave = picsFolder + picsToRotateFolder

if rotation != 0:
    print('Begin to rotate the pictures')
    picsNames = os.listdir(picsFolderToSave)
    for picName in picsNames:
        pic = Image.open(picsFolderToSave + '/' + picName)
        pic = pic.rotate(rotation, expand=1)
        pic.save(picsFolder + '/' + picName)
        print(picName + ' rotated')
    os.rmdir(picsFolderToSave)
    print('All pics moved in ' + picsFolder)

