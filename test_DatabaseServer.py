#OnCycle Project - Database Server Unit Test File
#--------------------------------------------------------------------------------------------------------
#Project: SYSC 3010 - OnCycle Project
#Author: Christian Sargusingh
#Date: 2018-11-22
#---------------------------------------------------------------------------------------------------------
#Description: This file contains all automated test cases for the Database Server Interface as detailed in
#the Test Plan Proposal

#import necessary libraries
import unittest, sys, time, serial, socket, pyrebase
#import the DatabaseServer class from DatabaseServer.py
from DatabaseServer import DatabaseServer

class TestDB(unittest.TestCase):
        
    def test_serialCollect(self):
        #configure firebase
        config = {
            "apiKey": "AIzaSyAnn-gvjSnif1mZ1IM1VGStOnECjXlHh7E",
            "authDomain": "oncycle-4654b.firebaseapp.com",
            "databaseURL": "https://oncycle-4654b.firebaseio.com/",
            "storageBucket": "oncycle-4654b.appspot.com"
        }
        firebase = pyrebase.initialize_app(config)
        #create a sample DatabaseServer object with an empty capture field
        self.db = DatabaseServer("10.0.0.51","5000",[],[],firebase.database())
        data = "256"
        self.assertEqual(DatabaseServer.serialCollect(self.db,data),False)

        #create a sample DatabaseServer object with an empty capture field
        capture = [247,342,256,124,287,293,238,321,153,156]
        self.db = DatabaseServer("10.0.0.51","5000",[],capture,firebase.database())
        data = "256"
        self.assertEqual(DatabaseServer.serialCollect(self.db,data),True)   

    def test_firebaseUpload(self):
        #configure firebase
        config = {
            "apiKey": "AIzaSyAnn-gvjSnif1mZ1IM1VGStOnECjXlHh7E",
            "authDomain": "oncycle-4654b.firebaseapp.com",
            "databaseURL": "https://oncycle-4654b.firebaseio.com/",
            "storageBucket": "oncycle-4654b.appspot.com"
        }
        firebase = pyrebase.initialize_app(config)
        #create a sample DatabaseServer object with an empty capture field
        self.db = DatabaseServer("10.0.0.51","5000",[],[],firebase.database())
        avgAcc = 234
        self.assertEquals(DatabaseServer.firebaseUpload(self.db,avgAcc),True)
        
    def test_udpReceive(self):
        #configure firebase
        config = {
            "apiKey": "AIzaSyAnn-gvjSnif1mZ1IM1VGStOnECjXlHh7E",
            "authDomain": "oncycle-4654b.firebaseapp.com",
            "databaseURL": "https://oncycle-4654b.firebaseio.com/",
            "storageBucket": "oncycle-4654b.appspot.com"
        }
        firebase = pyrebase.initialize_app(config)
        #create a sample DatabaseServer object with an empty capture field
        self.db = DatabaseServer("10.0.0.51","5000",[],[],firebase.database())
        #Define socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #bind the socket to the server address
        server_address = ("10.0.0.51",5000)
        s.bind(server_address)
        
        self.assertTrue(type(DatabaseServer.udpReceive(self.db, s, server_address)) == str)
        
#Check to see if the file is ran as a script or from a module
if __name__ == '__main__':
    unittest.main()
            

