#OnCycle Project - Network Controller Unit Test File
#--------------------------------------------------------------------------------------------------------
#Project: SYSC 3010 - OnCycle Project
#Author: Christian Sargusingh
#Date: 2018-11-22
#---------------------------------------------------------------------------------------------------------
#Description: This file contains all automated test cases for the Network Controller Interface as detailed
#in the Test Plan Proposal

#import necessary libraries
import unittest, socket, serial
#import the NetworkController class from NetworkController.py
from NetworkController import NetworkController

class TestNC(unittest.TestCase):
    #Define a setup method to define a NetworkController Object for each uni test
    def setUp(self):
        #create a sample NetworkController object
        self.nc = NetworkController("10.0.0.51", "5000","/dev/ttyUSB0")
        
    def test_serialRead(self):
        #create a sample serial object
        serial_port = "/dev/ttyUSB0"
        baud_rate = 9600
        ser = serial.Serial(serial_port, baud_rate)

        self.assertTrue(type(NetworkController.serialRead(self.nc,ser)) == str)

    def test_sendUDP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        line = "246"
        server_address = ("10.0.0.51", 5000)
        
        self.assertEquals(NetworkController.sendUDP(self.nc, s, line, server_address), True)
        
if __name__ == '__main__':
    unittest.main()

        
