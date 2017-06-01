import servo_drivers as driver
import segment as seg
import calc_dist as dist
import cv2
import os

IMAGE = "image.jpg"
PATH = os.getcwd()

def main():
	os.system('fswebcam -r 128x720 --no-banner ' + PATH + "/image.jpg")
	#Read image
	image = cv2.imread(IMAGE)
	qty, label, centers, width = seg.identify_target(seg.segment_img(image))
	calibrate = str(raw_input("Need to calibrate?: "))
	
	if calibrate == "y":
		knownDistance = int(input("How far is the object?: "))
		for item in width:		
			print(dist.calibrate(knownDistance, item))
 
if __name__ == '__main__':
    main()
