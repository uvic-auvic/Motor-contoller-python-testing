import serial, time

motor_string = 'M1F'

motor = serial.Serial(
	port='COM12',
	baudrate=9600,
	#parity=serial.None,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

def get_motor_instance():
	return motor

def set_forward():
	global motor_string
	motor_string = 'M1F'

def set_reverse():
	global motor_string
	motor_string = 'M1R'

def rev_down(max, min, delay):
	for i in range(max, min, -1):
		speed = i
		message = motor_string+chr(speed)+'\r\n'
		print("string out: " + message + " speed is: " + str(speed))
		motor.write(message.encode())
		time.sleep(delay)

def rev_up(min, max, delay):
	for i in range(min, max):
		speed = i
		message = motor_string+chr(speed)+'\r\n'
		print("string out: " + message + " speed is: " + str(speed))
		motor.write(message.encode())
		time.sleep(delay)

def set_speed(speed, do_print = False):
	if speed>110 or speed < 0:
		raise ValueError("Speed out of range: "+ str(speed))
	message = motor_string+chr(speed)+'\r\n'
	if do_print:
		print("string out: " + message + " speed is: " + str(speed))
	motor.write(message.encode())
	
def get_rpm():
	motor.reset_input_buffer()
	message = b"RV1\r\n"
	motor.write(message)
	revs = motor.read(4)
	rpm=(revs[1] * 255 + revs[0])
	return rpm

def stop():
	motor.write(b'STP\r\n')

def close():
	motor.close()
