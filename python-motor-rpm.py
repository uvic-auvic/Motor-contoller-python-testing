import time #libraries
import serial
import datetime
import threading

speed = 180

start = time.time()

sensor_port = 0
sensor_starboard = 0
sensor_front_1 = 0
sensor_front_2 = 0 
sensor_front = 0
sensor_back_1 = 0
sensor_back_2 = 0 
sensor_back = 0
const_star = 25
const_port = 26

motor_running_state = False 
motor_terminate = False

file = open("testfile.csv",'w') 
file.write("Time Since Start, Startboard, Port, Front, Back, RPM \n")

arduino = serial.Serial(
	port='COM7',
	baudrate=256000,
	#parity=serial.None,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)
#arduino.open()


motor = serial.Serial(
	port='COM6',
	baudrate=9600,
	#parity=serial.None,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

print("Serial opened")

def motor_run():
	print(time.ctime())
	if motor_running_state is True:
		message = 'M1R'+chr(speed)+'\r\n'
		try:
			motor.write(message.encode())
		except:
			print("Serial port probably closed")
	else:
		try:
			motor.write(motor.write(b'STP\r\n'))
		except:
			print("Serial port probably closed")
	if motor_terminate is True:
		exit()
	threading.Timer(1, motor_run).start()



motor_running_state = True


message = 'M1R'+chr(speed)+'\r\n'
motor.write(message.encode())



for k in range(10):
	i = arduino.readline()
	#print(str(i[0]))
	#print("Warming up")

#motor_run()

print("Motor task created")
message = 'M1R'+chr(speed)+'\r\n'
motor.write(message.encode())
time.sleep(1)
#message = 'M1R'+chr(speed)+'\r\n'
#motor.write(message.encode())
for k in range(50):
	print("start loop")
	message = 'M1R'+chr(speed)+'\r\n'
	motor.write(message.encode())
	#arduino.write(str.encode())
	arduino.flush()
	i = arduino.readline()
	
	try:
		motor.write(b'RVA\r\n')
		sensor_starboard = i[0]
		sensor_port = i[2]
		sensor_front_1 = i[4]
		sensor_front_2 = i[6] 
		sensor_back_1 = i[8]
		sensor_back_2 = i[10]
		x = motor.readline()
	except:
		print("Something went wrong")
		file.write("Err,Err,Err, Err, Err, Err \n")
	else:
		print("killing it")
		y = (x[2] * 255 + x[1])*60
		sensor_front = sensor_front_1 - sensor_front_2
		sensor_back = sensor_back_1 - sensor_back_2
		print("Sensor Starboard: ")
		
		print(sensor_starboard)
		"""
		print("Sensor Port: ")
		print(sensor_port)
		print( "Sensor Front: ")
		print (sensor_front)
		print( "Sensor Back: ")
		print (sensor_back)
		"""
		print ("RPM: ")
		print(y)
		current = time.time()
		elapsed = current - start
		file.write(str(elapsed) + ',')
		file.write(str(sensor_starboard) + ',')
		file.write(str(sensor_port) + ',')
		file.write(str(sensor_front) + ',')
		file.write(str(sensor_back) + ',')
		file.write(str(y) + '\n')
print("Done")
motor.write(b'STP\r\n')
motor.close()
file.close()
motor_running_state = False
motor_terminate = True
exit() 


#	for i in range(3):
#		time.sleep(1)
#		motor.write(b'RVA\r\n')
#		x = motor.readline()
#		y = (x[2] * 255 + x[1])*60
#		print(y)
#	motor.write(b'STP\r\n')
#	motor.close()

	
# configure the serial connections (the parameters differs on the device you are connecting to)