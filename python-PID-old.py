import time #libraries
import serial
import datetime
import threading
import motor_control
import math

arduino = serial.Serial(
	port='/dev/tty.usbmodem1411',
	baudrate=256000,
	#parity=serial.None,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

k=0
kd= 1
kp= 1
ki = 1

forward= 1
reverse = 0
Td= 0 #desired torque
density = 998.2 #kg/m^3
diameter = 0.07928 #m
k3 = 6*10^(-10) #must verify this value
direction = 0
#rpmd = math.sqrt(Td/(density*diameter^4*k3)) #calculates desired rpm from model and thrust input

sensor_back = 0
sensor_back_ADC =0
sensor_front = 0
sensor_front_ADC = 0
const_front = 57
const_back = 26

if direction == forward:
	motor_string = 'M1F'#gives intial value to motor string

if direction == reverse:
	motor_string = 'M1R'#gives intial value to motor string

speed = 0 #initial speed value

motor_running_state = False
motor_terminate = False

rpmd = 0 #sets desired RPM

i = arduino.readline() #reads force sensors
i = arduino.readline()
arduino.flush()
i = arduino.readline()

motor_running_state = False
motor_terminate = False

motor = motor_control.get_motor_instance()

if direction == forward:
	motor_control.set_forward() #sets direction

if direction == reverse:
	motor_control.set_reverse()

motor_running_state = True #turns motor on

file = open("testfile.csv",'w')
file.write("Time Since Start, Front, Front ADC, Back, Back ADC, RPM \n")

start = time.time()

for k<10000:
#bounds the command input
	k+=1
	arduino.reset_input_buffer()
	#first line may be gimped
	arduino.readline()
	i = arduino.readline()

	if direction== forward and speed>110:
		speed=110

	if direction== reverse and speed >80:
		speed=80

	if speed<30:
		speed == 0

	t1= time.time()
	rpm1=  (x[2] * 255 + x[1])*60
	time.sleep(0.000000001)
	t2= time.time()
	rpm2=  (x[2] * 255 + x[1])*60
	time.sleep(0.000000001)
	t3= time.time()
	rpm3=  (x[2] * 255 + x[1])*60
	time.sleep(0.000000001)
	t4= time.time()
	rpm4=  (x[2] * 255 + x[1])*60
	time.sleep(0.000000001)
	t5= time.time()
	rpm5=  (x[2] * 255 + x[1])*60
	time.sleep(0.000000001)

	speed = #PID line
	motor_control.set_speed(speed)

	try:
		motor.write(b'RVA\r\n')
		sensor_front = (i[2]-const_front)/2.9348
		sensor_front_ADC = i[2]
		sensor_back = (i[0]-const_back)/2.8563
		sensor_back_ADC = i[0]
		x = motor.readline()
	except:
		print("Something went wrong")
		file.write("Err,Err,Err, Err, Err, Err \n")
		print(i)
	else:
		rpm = (x[2] * 255 + x[1])*60 #i'm inconsistently getting out of range errors here

		if k % 25 == 0: #data is printed every 25 readings
			print( "Sensor Front: ")
			print (sensor_front)
			print( "Sensor Back: ")
			print (sensor_back)
			print ("RPM: ")
			print(rpm)
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
