import servo_drivers as driver
import segment as seg
import calc_dist as dist
import cv2
import os
import time
import argparse
from random import randint

IMAGE = "image.jpg"
PATH = os.getcwd()
fLength = 939.55
MID = 900
DELTA = 75
distance = []

def aimCake(coordinate, distance):
    x = coordinate[0]
    y = coordinate[1]
    delt = DELTA - (distance * 0.1)
    if x > MID:
        direction = driver.RIGHT
    else:
        direction = driver.LEFT
    while x > (MID + delt) or x < (MID - delt):
        driver.turnCake(direction)
        print("Moved")
        if direction:
            x += delt
        else:
            x -= delt
def calcPercentSpeed(distance):
    if distance > 100:
        return 100
    return int(distance)

def tiltAndLaunch(distance):
    temp = distance
    while temp > 0:
        driver.moveTilt(driver.UP)
        temp -= 20

    driver.launchBall(calcPercentSpeed(distance))

def main():
    parser = argparse.ArgumentParser(description='Ping Pong trainer that hits red targets')
    parser.add_argument('--numcycles', type=int, help='integer for number of cycles -- leave blank for infinite')
    parser.add_argument('--calibrate', dest='calibrate', action='store_true', help='use to calibrate camera')
    parser.add_argument('--delay', type=float, help='delay between shots -- default is 0') 
    parser.add_argument('--debug', dest='debug', action='store_true', help='enable image output')
    parser.set_defaults(numcycles=-1, calibrate=False, delay=0, debug=False)
    args = parser.parse_args()

    while args.numcycles > 0 or (args.numcycles <= -1 and args.calibrate == False):
        os.system('fswebcam -r 1920x1080 --no-banner ' + PATH + "/image.jpg")
        driver.setStartingWidth()
  #Read image
        image = cv2.imread(IMAGE)
        qty, label, centers, width = seg.identify_target(seg.segment_img(image))
        for each in centers:
            print(each)
        image = seg.augment_image(label, centers)
        if args.calibrate:
            knownDistance = int(input("How far is the object?: "))
            for item in width:
                print("New focal length is " + str(dist.calibrate(knownDistance, item)))
                return

        for item in width:
            distance.append(dist.distance_to_camera(fLength, item))
            print(dist.distance_to_camera(fLength, item))

        if args.debug:
            newx, newy = image.shape[1] / 4, image.shape[0] / 4
            newimage = cv2.resize(image, (int(newx), int(newy)))
            cv2.imshow("Image", newimage)
            cv2.waitKey(50)
            #cv2.waitKey(0)

    # Start shooting them randomly
        temp = randint(0, len(centers) - 1)
        aimCake(centers[temp], distance[temp])
        tiltAndLaunch(distance[temp])
        time.sleep(args.delay)
        args.numcycles -= 1

    driver.setStartingWidth()
if __name__ == '__main__':
    main()
