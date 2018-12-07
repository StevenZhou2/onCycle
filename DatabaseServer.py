#OnCycle Project - Database Server Interface
#--------------------------------------------------------------------------------------------------------
#Project: SYSC 3010 - OnCycle Project
#Author: Christian Sargusingh, Steven Zhou, Nathan Fohkens
#Date: 2018-11-22
#---------------------------------------------------------------------------------------------------------
#Description: This file contains the code for receiving accelerometer data from the NetworkController using
#UDP networking. This class is also responsible for grouping 10 accelerometer data points and computing an
#average analog value to determine the state of the device (whether it is turning or not).
#This boolean state will then be uploaded to firebase in real-time to then be pulled by the android device

#import necessary libraries
import sys, time, serial, socket, pyrebase

#firebase configuration
config = {  # recommnedation is to have this in a separeate config file
            # anyone can see this information and access our database and mess around with our database
    "apiKey": "AIzaSyAnn-gvjSnif1mZ1IM1VGStOnECjXlHh7E",
    "authDomain": "oncycle-4654b.firebaseapp.com",
    "databaseURL": "https://oncycle-4654b.firebaseio.com/",
    "storageBucket": "oncycle-4654b.appspot.com"
}
firebase = pyrebase.initialize_app(config)

class DatabaseServer(object):
    #DatabaseServer object fields
    host = ""
    textport = ""
    fdb = ""
    prev_capture = ""
    capture = ""
    
    
    #class initializer
    def __init__(self, host, textport, prev_capture, capture, fdb):
        from DatabaseServer import DatabaseServer
        self.host = host
        self.textport = textport
        self.prev_capture = prev_capture
        self.capture = capture
        self.fdb = fdb
            
    #Parse from sender to upload to firebase   
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
		#Variables from Arduino serial read
		leftState, brakeState, rightState, avgAcc = self.parseData(data)
                fullState = self.serialCollect(avgAcc)
                #if fullState is true then compute the average of the capture and upload to firebase
                if (fullState):
                    print ("Capture full, computing average acceleration...")
                    avgAcc = self.setAvgAcc(self.prev_capture)
                    #upload the average acceleration to firebase
                    print ("Uploading to Firebase...")
                    self.firebaseUpload(leftState, brakeState, rightState, avgAcc)
        #if a keyboard interrupt is detected then terminate server
        except KeyboardInterrupt:
            print("Server shutdown successful")
            
    #Intake data to average out
    #@param data Data to be averaged out
    #@return true if intake of 10 data points have been registered, otherwise false
    def serialCollect(self, data):
        #check if the capacity of capture has been reached. Then if it is full reset index purge the current capture and start a new capture list
        if (len(self.capture) == 10):
            self.prev_capture = self.capture
            del self.capture[:]
            self.capture.append(int(data))
            return True
        #convert next data point from str to int and then load into capture
        self.capture.append(int(data))
        return False

    #Upload average acceleration to firebase
    #@param leftState, brakeState, rightState, avgAcc Variables to upload to firebase
    #@return true if successful upload, otherwise false
    def firebaseUpload(self, leftState, brakeState, rightState, avgAcc):
        try:
	    self.fdb.child("data").update({"LeftState": leftState})
	    self.fdb.child("data").update({"RightState": rightState})
	    self.fdb.child("data").update({"BrakeState": brakeState})	
            self.fdb.child("data").update({"AvgAcc": avgAcc})
        except Exception as e:
            print(e)
            return False
        return True

    #Find average acceleration
    #@param prev_capture The list of the last 10 captured data
    #@return the average of the last 10 captured data
    def setAvgAcc(self, prev_capture):
        return sum(prev_capture)/len(prev_capture)
    
    #Read from port
    #@param s, server_address Parameters needed to know where to read from
    #@return the data sent from sender
    def udpReceive(self, s, server_address): 
        try:
            buf, address = s.recvfrom(2048)
            print ("Received %s bytes from %s %s: " % (len(buf), address, buf))
        except Exception as e:
            print(e)
            return 0
        return buf

    #Parse data received and place into proper variables
    #@param data The data being read in
    #@return leftState, rightState, brakeState, avgAcc Data placed into variables
    def parseData(self, data): 
        try:
	    splitDataList = data.split(" ");
	    leftState = int (splitDataList[0])
	    brakeState = int (splitDataList[1])
	    rightState = int (splitDataList[2])
	    avgAcc = int (splitDataList[3] + splitDataList[4] + splitDataList[5])
        except Exception as e:
            print(e)
            return 0
        return leftState, brakeState, rightState, avgAcc

#Initialization method - prompt input arguments
def main():
    #Host static IP Address (RPi1 static IP address: 10.0.0.52)
    host = raw_input('Enter the host IP Address: ')
    #Communication port (def. 5000)
    textport = raw_input('Enter Communication Port: ')
    #define capture fields for DatabaseServer
    capture = []
    prev_capture = []
    #Create firebase object
    fdb = firebase.database()
    #Create Database Server object
    db = DatabaseServer(host,textport, prev_capture, capture, fdb)
    #Start Serial IO Read
    db.parse()

#Check to see if the file is ran as a script or from a module
if __name__ == '__main__':
    main()
