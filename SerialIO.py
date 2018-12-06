#OnCycle Project - Network Controller Interface
#--------------------------------------------------------------------------------------------------------
#Project: SYSC 3010 - OnCycle Project
#Author: Christian Sargusingh, Steven Zhou
#Date: 2018-11-21
#---------------------------------------------------------------------------------------------------------
#Description: This file contains the code for retreiving the accelerometer data on a specified serial port
#and sending the values to the Database Server in real time.

#import necessary libraries
import socket, sys, time, serial

#Define input args for the python script
host = sys.argv[1]        #Host static IP Address (RPi3 static IP address: 10.0.0.51)
textport = sys.argv[2]    #Communication port (def. 5000)
serial_port = sys.argv[3] #Arduino IO serial port (def. /dev/ttyUSB0)

#Define socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)      #Convert String port to int
#Define server_address
server_address = (host, port)
baud_rate = 9600;         #NOTE baud rate should match baud rate in setup() in the arduino IDE "Serial.begin(9600)"
write_to_file_path = "output.txt";

#Define a write output file with overwrite
output_file = open(write_to_file_path, "w+");
#Define serial object using previous definitions
ser = serial.Serial(serial_port, baud_rate)

#Continually read data from the accelerometer printing whenever a serial exception occurs
while True:
    try:
        line = ser.readline();
        s.sendto(line, server_address)
        output_file.write(line);
        output_file.flush()
    #Overrides Serial Exception to prevent the read cycle from being halted
    except serial.SerialException:
        print("Serial Exception")
        output_file.write("N/A");
        
#Close all remaining resources
output_file.close();
s.shutdown(1)


