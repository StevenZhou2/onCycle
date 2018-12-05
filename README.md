# onCycle
Carleton University 3rd Year Computer Systems Engineering Project Course

This is a project created for the interest of SYSC3020. 

Proposal: https://docs.google.com/document/d/1WeDNtLlDCsHzvKkRGRF7GaEJgoGLFuDdTI8q8bofrOs/edit?usp=sharing

Final Report: #TOBEADDED

Android Program developed by: Steven Zhou

Arduino Code developed by: Christian Sargusingh

Database Controller developed by: Christian Sargusingh, Steven Zhou & Nathan Fohkens

Network Controller developed by: Christian Sargusingh & Steven Zhou

How to run the system:

Step 1: Launch RPi1 and run the Arduino C code

Step 2: Launch RPi2 and run the database interface with parameters 10.0.0.51 and 5000

Step 3: Within RPi1, run the network controller with parameteres 10.0.0.51, 5000 and /dev/ttyUSB0

Step 4: Ensure that internet is connected to RPi2 so that it can access the cloud database

Step 5: Launch the Android Application "onCycle" 

