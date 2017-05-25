from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Per tick 20ms / 4096 = 4.88us
TOTAL_TICKS = 4096
# 410 max ticks, 205 min ticks
MAX_TICKS = 410 
MIN_TICKS = 205
currHigh = []

def main():
	setStartingWidth
	
	while (1):
		command = input()
		
		if command == "w":
			# Tilt up 
			pwm.set_pwm(0, , 3072)
			
def setStartingWidth();
	startingHigh = (MAX_TICKS + MIN_TICKS) / 2
	startingLow = TOTAL_TICKS - startingHigh
	# Set servo frequency
	pwm.set_pwm_freq(50)
	for i in range(0,4):
		pwm.set_pwm(i, startingHigh, startingLow) 
	
def moveTilt(up):
	if up == True:
		if currHigh[0] < MAX_TICKS:
			pwm.set_pwm(0, currHigh[0] + 5, TOTAL_TICKS - currHigh[0] - 5)
	else:
		pwm.set_pwm(0, currHigh[0] - 5, TOTAL_TICKS - (currHigh[0] - 5))
		

if __name__ == '__main__':
	main()