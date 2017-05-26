from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Per tick 20ms / 4096 = 4.88us
MAX_TICKS = 4096
SERVO_MIN = 170
SERVO_MAX = 600
SERVO_MID = (SERVO_MIN + SERVO_MAX) // 2
DELTA = 10
LEFT = True
RIGHT = False

# Servos at different channels
TURN_SERVO = 0
TILT_SERVO = 1 
LOAD_SERVO = 2
RIGHT_MOTOR = 3
LEFT_MOTOR = 4

# Initializers
currVal = []
pwm = Adafruit_PCA9685.PCA9685()

def main():
	setStartingWidth()
	
	while (1):
		command = str(raw_input())
		
		if command == 'w':
			# Tilt up 
			moveTilt(True)	
		if command == 's':
			moveTilt(False)
		if command == 'e':
			launchBall()
		if command == 'a':
			turnCake(LEFT)
		if command == 'd':
			turnCake(RIGHT)
			
def setStartingWidth():
	#startingHigh = (MAX_TICKS + MIN_TICKS) / 2
	#startingLow = TOTAL_TICKS - startingHigh
	# Set servo frequency
	pwm.set_pwm_freq(60)
	for i in range(0,5):
		print(i)
		pwm.set_pwm(i, 0, SERVO_MID) 
		currVal.append(SERVO_MID)		
	
def moveTilt(up):
	if up == True:
		if currVal[TILT_SERVO] < SERVO_MAX:
			currVal[TILT_SERVO] += DELTA
			pwm.set_pwm(TILT_SERVO, 0, currVal[TILT_SERVO])
	else:
		if currVal[TILT_SERVO] > SERVO_MID:
			currVal[TILT_SERVO] -= DELTA
			pwm.set_pwm(TILT_SERVO, 0, currVal[TILT_SERVO])

def turnCake(left):
	if left:
		if currVal[TURN_SERVO] < SERVO_MAX:
			currVal[TURN_SERVO] += DELTA
			pwm.set_pwm(TURN_SERVO, 0, currVal[TURN_SERVO])
	else:
		if currVal[TURN_SERVO] > SERVO_MIN:
			currVal[TURN_SERVO] -= DELTA
			pwm.set_pwm(TURN_SERVO, 0, currVal[TURN_SERVO])

def increaseMotorSpeed(increase = True):
	if increase:
		pwm.set_pwm(LEFT_MOTOR, 0, MAX_TICKS - 1)		
		pwm.set_pwm(RIGHT_MOTOR, 0, MAX_TICKS - 1)
	else:
		pwm.set_pwm(LEFT_MOTOR, 0, 0)		
		pwm.set_pwm(RIGHT_MOTOR, 0, 0)
		
def launchBall():
	increaseMotorSpeed()
	time.sleep(1.75)
	pwm.set_pwm(LOAD_SERVO, 0, SERVO_MAX)
	time.sleep(.35)
	pwm.set_pwm(LOAD_SERVO, 0, SERVO_MID)
	time.sleep(.25)
	increaseMotorSpeed(False)
	
if __name__ == '__main__':
	main()
