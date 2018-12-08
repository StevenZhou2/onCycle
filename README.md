Carleton University 3rd Year Computer Systems Engineering Project Course

Note: The user “ILoveEatingRice” commits are Steven Zhou's old GitHub account.

This is a project created for the interest of SYSC3010.

Final Report: https://docs.google.com/document/d/1Fyc9J35bfsdD_GmBIRzxaPumELoXXPGDXqmJ-pHRuV4/edit?usp=sharing

GitHub: https://github.com/StevenZhou2/onCycle 

Link to onCylce’s cloud database, Firebase: https://console.firebase.google.com/u/0/project/oncycle-4654b/database/oncycle-4654b/data 

Android Program developed by: Steven Zhou

Arduino Code developed by: Christian Sargusingh

Database Controller developed by: Christian Sargusingh, Steven Zhou, & Nathan Fohkens

Network Controller developed by: Christian Sargusingh & Steven Zhou

Roadmap of code repository:

Arduino C Code: onCycle/OnCycle_Arduino_Interface.ino

Database Interface: onCycle/DatabaseInterface.py

Network Controller: onCycle/NetworkController.py

Android Application: onCycle/app/src/main/java/com/example/noric/oncycle/MainActivity.java

How to run the system:

Step 1: Launch RPi1 and run the Arduino C code

Step 2: Launch RPi3 and run the Database Interface with parameters 10.0.0.51 and 5000

Step 3: Within RPi1, run the Network Controller with parameters 10.0.0.51, 5000 and /dev/ttyUSB0

Step 4: Ensure that internet is connected to RPi3 so that it can access the cloud database

Step 5: Launch the Android Application "onCycle"
