import RPi.GPIO as io
import sys

io.setmode(io.BCM)
io.setup(23,io.IN,pull_up_down=io.PUD_UP)
io.setup(24,io.IN,pull_up_down=io.PUD_UP)
io.setup(25,io.IN,pull_up_down=io.PUD_UP)

input("Press and hold the switch and hit enter when ready")
b1 = io.input(23)
b2 = io.input(24)
b3 = io.input(25)

print("1 means up, 0 means down")
print('Button 1 is %s', b1)
print('Button 2 is %s', b2)
print('Button 3 is %s', b3)
