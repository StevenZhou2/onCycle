#OnCycle Project - Database Server Interface
#--------------------------------------------------------------------------------------------------------
#Project: SYSC 3010 - OnCycle Project
#Author: Christian Sargusingh
#Date: 2018-11-22
#---------------------------------------------------------------------------------------------------------
#Description: This file contains the code for receiving accelerometer data from the NetworkController using
#UDP networking. This class is also responsible for grouping 10 accelerometer data points and computing an
#average analog value to determine the state of the device (whether it is turning or not).
#This boolean state will then be uploaded to firebase in real-time to then be pulled by the android device

#import necessary libraries
import sys, time, serial, socket

#define storage array of ten elements for average captures
CAPTURE_CAPACITY = 10
prev_capture = [None]*CAPTURE_CAPACITY
capture = [None]*CAPTURE_CAPACITY
index = 0


class DatabaseServer(object):
    #DatabaseServer object fields
    host = ""
    textport = ""
    
    #class initializer
    def __init__(self, host, textport):
        from DatabaseServer import DatabaseServer
        self.host = host
        self.textport = textport
        
    def parse(self):
        #Define socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #Convert String port to int
        port = int(self.textport)
        #Define server_address
        server_address = (self.host, port)
        #bind the socket to the server address
        s.bind(server_address)
        
        #Read data from the accelerometer continouslly until a keyboard interrupt occurs
        try:    
            while True:
                print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop" % port)
                data = self.udpReceive(s, server_address)
                if not len(buf):
                    break
                print ("Received %s bytes from %s %s: " % (len(buf), address, buf))
                fullState = self.serialCollect(data)
                print ("Capture full, computing average acceleration...")
                #if fullState is true then compute the average of the capture and upload to firebase
                if (fullState):
                    avgAcc = self.setAvgAcc(prev_capture)
                    #upload the average acceleration to firebase
                    print ("Uploading to Firebase...")
                    self.firebaseUpload(avgAcc)
        #if a keyboard interrupt is detected then terminate server
        except KeyboardInterrupt:
            print("Server shutdown successful")

    def serialCollect(self, data):
        #check if the capacity of capture has been reached. Then if it is full reset index purge the current capture and start a new capture list
        if (capture[CAPTURE_CAPACITY-1] != None):
            prev_capture = capture
            capture = [None]*CAPTURE_CAPACITY
            index = 0
            capture[index] = int(data)
            return True
        #convert next data point from str to int and then load into capture
        capture[index] = int(data)
        #increment capture index
        index = index + 1
        return False

    def firebaseUpload(self):
        return
        
    def setAvgAcc(self, prev_capture):
        return sum(prev_capture)/len(prev_capture)
    
    def udpReceive(self, s, server_address): 
        try:
            buf, address = s.recvfrom(2048)
        except Exception as e:
            print(e)
            return 0
        return buf
    
#Initialization method - prompt input arguments
def main():
    #Host static IP Address (RPi1 static IP address: 10.0.0.52)
    host = raw_input('Enter the host IP Address: ')
    #Communication port (def. 5000)
    textport = raw_input('Enter Communication Port: ')
    #Create Database Server object
    db = DatabaseServer(host,textport)
    #Start Serial IO Read
    db.parse()

#Check to see if the file is ran as a script or from a module
if __name__ == '__main__':
    main()
            

