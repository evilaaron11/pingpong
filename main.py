import servo_drivers as driver
import segment as seg
import cv2
import os

IMAGE = "image.jpg"
PATH = os.cwd()

def main():
	os.system('fswebcam ' + PATH)
	#Read image
	image = cv2.imread(IMAGE)
	qty, label, centers, width = seg.identify_target(seg.segment_img(image))

