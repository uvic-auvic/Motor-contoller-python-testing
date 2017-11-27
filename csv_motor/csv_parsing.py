import sys
import csv
import time

def set_motor(motor, side, direction, speed):
	print(motor + side + direction + str(speed))

#The order is going to be FL, FR, UL, UR, BL, BR
Motors = ["Front", "Depth", "Back"]
Sides = ["Left", "Right"]
Directions = ["Forward", "Reverse"]

with open(sys.argv[1], 'r') as fh2:
	reader = csv.reader(fh2)
	for row in reader:
		if row[1] == "F":
			motor_set("Front", "Left", "Forward", row[2])
		else:
			motor_set("Front", "Left", "Reverse", row[2])
		if row[3] == "F":
			motor_set("Front", "Right", "Forward", row[4])
		else:
			motor_set("Front", "Right", "Reverse", row[4])
		if row[5] == "F":
			motor_set("Depth", "Left", "Forward", row[6])
		else:
			motor_set("Depth", "Left", "Forward", row[6])
		if row[7] == "F":
			motor_set("Depth", "RIght", "Reverse", row[8])
		else:
			motor_set("Depth", "Right", "Reverse", row[8])
		if row[9] == "F":
			motor_set("Back", "Left", "Forward", row[10])
		else:
			motor_set("Back", "Left", "Forward", row[10])
		if row[11] == "F":
			motor_set("Back", "Right", "Reverse", row[12])
		else:
			motor_set("Back", "Right", "Reverse", row[12])
		time.sleep(row[0])
			
		"""
		i = 0
		for m in Motors:
			for s in Sides:
				if row[1+2*i] == 'F':
					motor_set(m, s, "For
					i += 1
		"""