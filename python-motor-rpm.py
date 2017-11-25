import time #libraries
import serial
import datetime
import threading
import motor_control

speed = 40 #forward max:110 min:30 #back max:80 min:30

data_loops = 500

start = time.time()

sensor_back = 0
sensor_back_ADC =0
sensor_front = 0
sensor_front_ADC = 0
const_front = 58
const_back = 25

#motor_string = 'M1F'

motor_running_state = False
motor_terminate = False

file = open("testfile.csv",'w')
file.write("Time Since Start, Front, Front ADC, Back, Back ADC, RPM \n")

arduino = serial.Serial(
	port='/dev/tty.usbmodem1421',
	baudrate=256000,
	#parity=serial.None,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)
#arduino.open()

motor = motor_control.get_motor_instance()
motor_control.set_reverse()

print("Serial opened")

motor_running_state = True

motor_control.rev_up(30, speed, 0.1)

for i in range(2):
	motor_control.set_speed(speed)
	time.sleep(1)

arduino.flush()

print("start loop")
for current_loop in range(data_loops):
	motor_control.set_speed(speed)

	arduino.reset_input_buffer()
	arduino.write(b'R')
	#first line may be gimped
	arduino_adc = arduino.read(4)

	try:
		motor.write(b'RV1\r\n')
		sensor_front = (arduino_adc[0]-const_front)/2.9348
		sensor_front_ADC = arduino_adc[0]
		sensor_back = (arduino_adc[1]-const_back)/2.8563
		sensor_back_ADC = arduino_adc[1]
		revs = motor.read(4)
		motor.reset_input_buffer()
	except:
		print("Something went wrong")
		file.write("Err,Err,Err, Err, Err, Err \n")
		print(arduino_adc)
	else:
		#print(revs)
		rpm = (revs[1] * 255 + revs[0])
		#print (revs)
		if current_loop % 50 == 0:
			percent = int(100 * float(current_loop)/float(data_loops))
			print(str(percent) + "% done")
			print( "Sensor Front: " + str(sensor_front))
			print( "Sensor Back: " + str(sensor_back))
			print ("RPM: " + str(rpm))
		current = time.time()
		elapsed = current - start
		file.write(str(elapsed) + ',')
		file.write(str(sensor_front) + ',')
		file.write(str(sensor_front_ADC) + ',')
		file.write(str(sensor_back) + ',')
		file.write(str(sensor_back_ADC) + ',')
		file.write(str(rpm) + '\n')
print("Done")
motor.write(b'STP\r\n')
motor.close()
file.close()
exit()
