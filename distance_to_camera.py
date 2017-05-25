import numpy as npy
import cv2
import time

def find_target(image):
    #convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    edged = cv2.Canny(gray, 35, 125)

    #find contours and keep largest one?? from tutorial
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)

    return cv2.minAreaRect(c)


def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth


# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 45.0

# initialize the known object width, which in this case, the piece of
# paper is 11 inches wide
KNOWN_WIDTH = 3.1

# initialize the list of images that we'll be using
IMAGE_PATHS = ["samples/IMG_20170430_210143.jpg"]
#, "IMG_20170426_193126.jpg"]

# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = cv2.imread(IMAGE_PATHS[0])
marker = find_target(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

# loop over the images
for imagePath in IMAGE_PATHS:
    # load the image, find the ma  rker in the image, then compute the
    # distance to the marker from the camera
    image = cv2.imread(imagePath)
    marker = find_target(image)
    print(marker[1][0])
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])

    # draw a bounding box around the image and display it
    box = npy.int0(cv2.boxPoints(marker))
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv2.putText(image, "%.2fft" % (inches / 12),
                (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (0, 255, 0), 3)
    newx, newy = image.shape[1] / 6, image.shape[0] / 6
    newimage = cv2.resize(image, (int(newx), int(newy)))
    cv2.imshow("image", newimage)

    cv2.resizeWindow("image", 500, 500)
    print(imagePath)
    cv2.waitKey(0)

cv2.destroyAllWindows()