#OnCycle Project - Network Controller Interface
#--------------------------------------------------------------------------------------------------------
#Project: SYSC 3010 - OnCycle Project
#Author: Christian Sargusingh, Steven Zhou
#Date: 2018-11-21
#---------------------------------------------------------------------------------------------------------
#Description: This file contains the code for retreiving the accelerometer data and button states on a specified serial port
#and sending the values to the Database Server in real time.

#import necessary libraries
import socket
import sys, time, serial


class NetworkController(object):
    #Network Controller object fields
    host = ""
    textport = ""
    serial_port = ""
    
    #class initializer
    def __init__(self, host, textport, serial_port):
        from NetworkController import NetworkController
        self.host = host
        self.textport = textport
        self.serial_port = serial_port
        
    #Reads data from Arduino and sends to RPi3    
    def serialIO(self):
        #Define socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #Convert String port to int
        port = int(self.textport)
        #Define server_address
        server_address = (self.host, port)
        #NOTE baud rate should match baud rate in setup() in the arduino IDE "Serial.begin(9600)"
        baud_rate = 9600;
        
        #Define serial object using previous definitions
        ser = serial.Serial(self.serial_port, baud_rate)
        
        #Read data from the accelerometer continouslly until a keyboard interrupt occurs
        try:    
            while True:
                line = self.serialRead(ser)
                sendStatus = self.sendUDP(s, line, server_address)
        #if a keyboard interrupt is detected then terminate serialIO read
        except KeyboardInterrupt:
            print("Client shutdown successful")

    #Reads from Arduino serial monitor and returns the value
    #@param ser The serial that we are reading from
    #@return the value from the serial 
    def serialRead(self, ser):
        try:
            getValue = ser.readline()
            return getValue
        #Overrides Serial Exception to prevent the read cycle from being halted
        except serial.SerialException:
            print("Serial Exception")
            return 0
    
    #Sends the data to RPi3
    #@param s, line, server_address sends data, line, to the given socket and server address
    #@return true if successful send, re
    def sendUDP(self, s, line, server_address): 
        try:
            s.sendto(line, server_address)
        except Exception as e:
            print(e)
            return False
        return True
    
#Initialization method - prompt input arguments
def main():
    #Host static IP Address (RPi3 static IP address: 10.0.0.51)
    host = raw_input('Enter the host IP Address: ')
    #Communication port (def. 5000)
    textport = raw_input('Enter Communication Port: ')
    #Arduino IO serial port (def. /dev/ttyUSB0)
    serial_port = raw_input('Enter Hardware Serial Port: ')
    #Create Network controller object
    nc = NetworkController(host,textport,serial_port)
    #Start Serial IO Read
    nc.serialIO()

#Check to see if the file is ran as a script or from a module
if __name__ == '__main__':
    main()
