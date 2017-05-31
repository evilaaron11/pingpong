# Width of the target
# The red targets are 3in in diameter
ITEM_WIDTH = 3

def calibrate(distance, pixelWidth):
	return (distance * pixelWidth) / ITEM_WIDTH

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth
