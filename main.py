import servo_drivers as driver
import segment as seg
import calc_dist as dist
import cv2
import os

IMAGE = "image.jpg"
PATH = os.cwd()

def main():
	os.system('fswebcam ' + PATH)
	#Read image
	image = cv2.imread(IMAGE)
	qty, label, centers, width = seg.identify_target(seg.segment_img(image))
	calibrate = input("Need to calibrate?: ")
	
	if calibrate == "y":
		knownDistance = int(input("How far is the object?: "))
		for item in width:		
			print(dist.calibrate(knownDistance, item))
 
