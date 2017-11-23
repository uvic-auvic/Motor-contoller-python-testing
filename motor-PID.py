import time #libraries
import serial
import datetime
import threading
import motor_control
import math

k=0
ie=0

#PID values
kd= 0.0002
kp= 0.007
ki =  0.0045
#0.0001

#thruster model
Td= 0 #desired torque
density = 998.2 #kg/m^3
diameter = 0.07928 #m
k3 = 6*10^(-10) #must verify this value
#rpmd = math.sqrt(Td/(density*diameter^4*k3)) #calculates desired rpm from model and thrust input
rpmd = 5000

#motor direction
forward= 1
reverse = 0
direction = forward #sets motor direction

#command input
speed = 0 #inital speed value

#number of cycles
data_loops = 400

start = time.time()

#sensor reading intializations
sensor_back = 0
sensor_back_ADC =0
sensor_front = 0
sensor_front_ADC = 0
const_front = 58
const_back = 25

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

if direction == forward:
	motor_control.set_forward()
if direction == reverse:
	motor_control.set_reverse()

print("Serial opened")

motor_running_state = True

for i in range(2):
	motor_control.set_speed(speed)
	time.sleep(1)

arduino.flush()

print("start loop")
for current_loop in range(data_loops):

	if direction== forward and speed>110:
		speed=110

	if direction== reverse and speed >80:
		speed=80

	if speed<30:
		speed = 0

	motor_control.set_speed(int(speed))

	arduino.reset_input_buffer()
	arduino.write(b'R')

	#first line may be gimped
	arduino_adc = arduino.read(4)

	motor.write(b'RV1\r\n')
	revs = motor.read(4)
	motor.reset_input_buffer()
	t1= time.time()
	rpm1=  (revs[1] * 255 + revs[0])
	e1 = rpmd-rpm1

	motor.write(b'RV1\r\n')
	revs = motor.read(4)
	motor.reset_input_buffer()
	t2= time.time()
	rpm2=  (revs[1] * 255 + revs[0])
	e2 = rpmd-rpm2

	motor.write(b'RV1\r\n')
	revs = motor.read(4)
	motor.reset_input_buffer()
	t3= time.time()
	rpm3=  (revs[1] * 255 + revs[0])
	e3 = rpmd-rpm3

	motor.write(b'RV1\r\n')
	revs = motor.read(4)
	motor.reset_input_buffer()
	t4= time.time()
	rpm4=  (revs[1] * 255 + revs[0])
	e4 = rpmd-rpm4

	motor.write(b'RV1\r\n')
	revs = motor.read(4)
	motor.reset_input_buffer()
	t5= time.time()
	rpm5=  (revs[1] * 255 + revs[0])
	e5 = rpmd-rpm5

	avgrpm = (rpm1+rpm2+rpm3+rpm4+rpm5)/5
	print ("Measured RPM: " + str(avgrpm))

	e = rpmd - avgrpm #error term
	print ("Error Term: " + str(e))

	dt = ((t5-t4)+(t4-t3)+(t3-t2)+(t2-t1))/4 #change in time per reading
	de = (-e5+8*e4-8*e2+e1)/(12*dt) #derivative term
	print ("Diff Term: " + str(de))

	ie = ie+((t2-t1)*(e1+e2)/2)+((t3-t2)*(e3+e2)/2)+((t4-t3)*(e3+e4)/2)+((t5-t4)*(e5+e4)/2) #integral term
	print ("Integral Term: " + str(ie))
	command = kp*e+ki*ie+kd*de #PID line
	speed = 0.81*command+29
	speed= int(speed)
	print ("Speed: " + str(speed))

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
print("STP")
motor.close()
file.close()
exit()
