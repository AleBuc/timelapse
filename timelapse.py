import asyncio
import os
import shutil
from datetime import datetime
from os import system

from PIL import Image
from picamera import PiCamera

totalTime = 5  # set the total time of capture in minutes
capturePeriod = 5  # set the period in seconds between 2 taken pictures
rotation = 270  # set the angle of rotation needed for the pictures.
fps = 60  # set number of frames per second of the video
xResolution = 1000
yResolution = 1000
picturesDirectory = '/home/pi/Pictures'
videosDirectory = '/home/pi/Videos'


async def capture(camera, picsFolderToSave, i, numPics):
    camera.capture(picsFolderToSave + '/img{0:05d}.png'.format(i), format='png')
    print('Capture ' + str(i) + ' on ' + str(numPics) + '.')


async def waiting(seconds):
    await asyncio.sleep(seconds)


def calibration(camera,picsFolderToSave):
    calibrationPath = picsFolderToSave + '/img_calibration.png'
    date1 = datetime.now()
    camera.capture(calibrationPath, format='png')
    date2 = datetime.now()
    os.remove(calibrationPath)
    return (date2-date1).total_seconds()


async def main():
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
    correctPeriod = capturePeriod - calibration(camera, picsFolderToSave)
    print('Begin the capture at ' + datetime.now().isoformat() + '.')
    for i in range(numPics):
        await asyncio.create_task(capture(camera, picsFolderToSave, i, numPics))
        await asyncio.create_task(waiting(correctPeriod))
    print(str(range) + ' taken pictures at ' + datetime.now().isoformat() + '.')

    if rotation != 0:
        print('Begin to rotate the pictures')
        picsNames = os.listdir(picsFolderToSave)
        for picName in picsNames:
            pic = Image.open(picsFolderToSave + '/' + picName)
            pic = pic.rotate(rotation, expand=1)
            pic.save(picsFolder + '/' + picName)
            print(picName + ' rotated')
        shutil.rmtree(picsFolderToSave)
        print('All pics moved in ' + picsFolder)

    print('Begin video creation')
    videoName = '{}.mp4'.format(date)
    system('ffmpeg -r {} -f image2 -s '.format(fps) + str(xResolution) + 'x' + str(
        yResolution) + ' -nostats -loglevel 0 -pattern_type glob -i "' + picsFolder + '/*.png" -vcodec libx264 -crf 25  -pix_fmt yuv420p ' + videosDirectory + '/' + videoName)
    print('Video creation finished with name {}'.format(videoName))


asyncio.run(main())
