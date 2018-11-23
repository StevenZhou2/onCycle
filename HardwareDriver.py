#OnCycle Project - ADXL345 Hardware Driver Test File
#--------------------------------------------------------------------------------------------------------
#Project: SYSC 3010 - OnCycle Project
#Author: Christian Sargusingh
#Date: 2018-11-22
#---------------------------------------------------------------------------------------------------------
#Description: This file contains all automated test cases for the ADXL345

#import necessary libraries
import unittest, serial
#import the NetworkController class from NetworkController.py
from NetworkController import NetworkController

class HardwareDriver(unittest.TestCase):
    #Define a setup method to define a NetworkController Object for each uni test
    def setUp(self):
        #create a sample NetworkController object
        self.nc = NetworkController("10.0.0.51", "5000","/dev/ttyUSB0")
        
    def test_serialRead(self):
        #create a sample serial object
        serial_port = "/dev/ttyUSB0"
        baud_rate = 9600
        ser = serial.Serial(serial_port, baud_rate)
        #assert that serialRead returns a string
        self.assertTrue(type(NetworkController.serialRead(self.nc,ser)) == str)
        #assert a non-negative return
        self.assertTrue(int(NetworkController.serialRead(self.nc,ser)) > 0)
        #assert a number that is not greater than the range of analog measurments
        self.assertTrue(int(NetworkController.serialRead(self.nc,ser)) < 1200)
        
if __name__ == '__main__':
    unittest.main()

        
