import asyncio
import os
import shutil
from datetime import datetime
from datetime import timedelta
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


async def capture(camera, pics_folder_to_save, i, num_pics):
    camera.capture(pics_folder_to_save + '/img{0:05d}.png'.format(i), format='png')
    print('Capture ' + str(i) + ' on ' + str(num_pics) + '.')


async def waiting(cycle_beginning_time, cycle_duration):
    now = datetime.utcnow()
    cycle_end = cycle_beginning_time + timedelta(seconds=cycle_duration)
    time_delta = cycle_end - now
    await asyncio.sleep(time_delta.total_seconds())


def calibration(camera, pics_folder_to_save):
    calibration_path = pics_folder_to_save + '/img_calibration.png'
    date1 = datetime.utcnow()
    camera.capture(calibration_path, format='png')
    date2 = datetime.utcnow()
    os.remove(calibration_path)
    return (date2-date1).total_seconds()


async def main():

    camera = PiCamera()
    camera.resolution = (xResolution, yResolution)

    date = datetime.utcnow().isoformat()
    if rotation == 0:
        pics_to_rotate_folder = ''
    else:
        pics_to_rotate_folder = '/to_rotate'

    pics_folder = picturesDirectory + '/picsTaking' + date
    pics_folder_to_save = pics_folder + pics_to_rotate_folder
    os.mkdir(pics_folder)

    if rotation != 0:
        os.mkdir(pics_folder_to_save)
    calibration_duration = calibration(camera, pics_folder_to_save)
    if calibration_duration > capturePeriod:
        new_capture_period = calibration_duration
    else:
        new_capture_period = capturePeriod

    num_pics = int((totalTime * 60) / new_capture_period)  # number of pictures to take
    print(str(num_pics) + ' pictures to take.')

    print('Begin the capture at ' + datetime.utcnow().isoformat() + '.')
    taken_pics = 0
    for i in range(num_pics):
        cycle_beginning = datetime.utcnow()
        await asyncio.create_task(capture(camera, pics_folder_to_save, i, num_pics))
        if new_capture_period != calibration_duration:
            await asyncio.create_task(waiting(cycle_beginning, new_capture_period))
        taken_pics += 1
    print(str(taken_pics) + ' taken pictures at ' + datetime.utcnow().isoformat() + '.')

    if rotation != 0:
        print('Begin to rotate the pictures')
        pics_names = os.listdir(pics_folder_to_save)
        for pic_name in sorted(pics_names):
            pic = Image.open(pics_folder_to_save + '/' + pic_name)
            pic = pic.rotate(rotation, expand=True)
            pic.save(pics_folder + '/' + pic_name)
            print(pic_name + ' rotated')
        shutil.rmtree(pics_folder_to_save)
        print('All pics moved in ' + pics_folder)

    print('Begin video creation')
    video_name = '{}.mp4'.format(date)
    system('ffmpeg -r {} -f image2 -s '.format(fps) + str(xResolution) + 'x' + str(
        yResolution) + ' -nostats -loglevel 0 -pattern_type glob -i "' + pics_folder +
           '/*.png" -vcodec libx264 -crf 25  -pix_fmt yuv420p ' +
           videosDirectory + '/' + video_name)
    print('Video creation finished with name {}'.format(video_name))


asyncio.run(main())
