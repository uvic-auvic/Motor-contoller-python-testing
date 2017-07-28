import csv
import sys
import time 
import serial
import datetime
import threading

#global vars
speed = 100

#motor stuff
def doMotors(time, dir, speed):
    left_motor = serial.Serial(
	    port='/dev/ttyUSB0',
	    baudrate=9600,
	    #parity=serial.None,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
    )




    right_motor = serial.Serial(
	    port='/dev/ttyUSB1',
	    baudrate=9600,
	    #parity=serial.None,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
    )
    print "MOTORS DONE"
#function space

def UP():
    return 0

def DOWN():
    return 0

def FORWARD():
    return 0

def REVERSE():
    return 0

def parse_csv():
    pass
    if sys.argv[1] == '2.csv':
        #floats
        f = open(sys.argv[1], 'rt')
        try:
            reader = csv.reader(f)
            for row in reader:
                print row
                print float(row[0]) + float(row[1])
        finally:
            f.close()
    elif sys.argv[1] == '1.csv':
        #static commands
        f = open(sys.argv[1], 'rt')
        try:
            reader = csv.reader(f)
            for row in reader:
                print row
                doMotors(row[0], row[1], row[2])
        finally:
            f.close()


#main
def runMotors(time, dir, speed):
    while True:
        #print "To run program, enter 'continue' as command"
        #print "To close program, enter something that's not 'continue'"
        #x = raw_input("Enter Command\r\n")
        #if x != 'continue':
        #    return 0
        #print "continue with program"



#run space
parse_csv()

