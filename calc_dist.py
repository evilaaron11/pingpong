# Width of the target
# The red targets are 3in in diameter
ITEM_WIDTH = 3

def calibrate(distance, pixelWidth):
	return (distance * pixelWidth) / ITEM_WIDTH

def distance_to_camera(focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (ITEM_WIDTH * focalLength) / perWidth
