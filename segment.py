import cv2
import numpy as np
from scipy import ndimage

IMAGE = "samples/red_stickers.jpg"
KNOWN_WIDTH = 3
NEXUS_FL = 600
#"samples/single_red.jpg"
#"samples/IMG_20170430_210143.jpg"
#"samples/IMG_20170430_202338.jpg"
#"samples/IMG_20170426_193046.jpg"
#"samples/IMG_20170423_194446.jpg"
#"samples/IMG_20170423_194339.jpg"
#"samples/IMG_20170426_193046.jpg"

def segment_img(img):
    """
    Attempts to produce a mask that isolates the avocados in the provided
    image by analyzing Luminance color channel.
    """
    transform = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, sat, value = cv2.split(transform)

    #blur = cv2.GaussianBlur(hue, (7, 7), 0)
    #median_hue = np.median(blur)
    #low = int(0.751 * median_luminance + 115)
    #high = 255
    # lower mask (0-10)
    # lower_red = np.array([0, 50, 50])
    # upper_red = np.array([10, 255, 255])
    # mask0 = cv2.inRange(transform, lower_red, upper_red)

    # upper mask (170-180)
    #lower_red = np.array([170, 50, 50])
    #upper_red = np.array([180, 255, 255])
    lower_red = np.array([0, 150, 150])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(transform, lower_red, upper_red)
    #mask = mask0 + mask1

    # lower_white = np.array([10, 10, 60])
    # upper_white = np.array([40, 40, 90])
    # mask2 = cv2.inRange(transform, lower_white, upper_white)
    #mask = blur
    return mask1

def is_target(contour):
    """
    Accepts a contour and classifies it as an avocado or non-avocado based
    on its area and circularity.
    :param contour: The contour to classify
    :return: True if classified as an avocado, otherwise False
    """
    area = cv2.contourArea(contour)
    convex = cv2.convexHull(contour)
    perimeter = cv2.arcLength(convex, closed=True)
    circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
    return area > 100 and circularity > 0.5, perimeter

def identify_target(img):
    _, cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    labeled, qty = ndimage.label(img)
    labeled_normalized = np.multiply(labeled, 255 / (labeled.max() + 1)).astype(np.uint8)

    centers = []
    width = []
    for contour in cnts:
        target, perimeter = is_target(contour)
        if target:
            print(cv2.contourArea(contour))
            moment = cv2.moments(contour)
            x = int(moment["m10"] / moment["m00"])
            y = int(moment["m01"] / moment["m00"])
            centers.append((x, y))
            print("{}, {}" .format(x,y))
            width.append(perimeter / 3.14)
            print("Width is ", perimeter / 3.14)

    colored = cv2.applyColorMap(labeled_normalized, cv2.COLORMAP_JET)

    return qty, colored, centers, width

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

def augment_image(labeled, centers):
        """
        Augments the labeled frame for debug purposes. Circles the provided centers.
        :param labeled: The labeled version of the frame
        :param centers: A list of (x, y) centers identified in the frame
        :return: The augmented frame
        """
        # Operations will mutate image, copy to preserve original
        augmented = labeled.copy()

        w = labeled.shape[1]
        h = labeled.shape[0]

        # Circle centers
        for x, y in centers:
            cv2.circle(augmented, (int(x), int(y)), radius=10, thickness=3, color=(255, 255, 255))

        return augmented

def main():

    # Read image
    image = cv2.imread(IMAGE)
    # newx, newy = image.shape[1] / 6, image.shape[0] / 6
    # image = cv2.resize(image, (int(newx), int(newy)))
    #comment here
    #image = segment_img(image)
    #cv2.imshow("orig", image)
    qty, label, centers, width = identify_target(segment_img(image))
    image = augment_image(label, centers)
    for item in width:
        print(distance_to_camera(KNOWN_WIDTH, NEXUS_FL, item))
    newx, newy = image.shape[1] / 3, image.shape[0] / 3
    newimage = cv2.resize(image, (int(newx), int(newy)))
    cv2.imshow("Keypoints", newimage)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
