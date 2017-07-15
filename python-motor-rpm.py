import time
import serial

speed = 128

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    #parity=serial.None,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()
str = 'M1R'+chr(speed)+'\r\n'
ser.write(str.encode())
for i in range(3):
	time.sleep(1)
	ser.write(b'RVA\r\n')
	x = ser.readline()
	y = (x[2] * 255 + x[1])*60
	print(y)
ser.write(b'STP\r\n')
ser.close()