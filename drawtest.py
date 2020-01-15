import sys
import time
from pyaxidraw import axidraw
import random

def do_move_benchmark(adl, x, y, numMeasurements):
    print("Measuring time to move to", x, ",", y, "from 0 , 0")

    measurements = [];
    
    for i in range(numMeasurements):
        startTime = time.time()
        adl.moveto(x, y)
        measurements.append(time.time() - startTime);
        adl.moveto(0,0)

    print("Took", sum(measurements) / len(measurements), "on average");

# Initialize class
ad = axidraw.AxiDraw() 

# Enter interactive mode
ad.interactive()

# Open serial port to AxiDraw 
connected = ad.connect()

if not connected:
    print("There is no AxiDraw plugged in.")

    # end script
    sys.exit()

print("Connected to AxiDraw device.")

ad.options.speed_penup = 110
ad.options.speed_pendown = 110
ad.options.accel = 100
ad.options.model = 1
ad.update()

for i in range(50):
    ad.penup()
    ad.pendown()

#do_move_benchmark(ad, 11.81, 0, 50)
#do_move_benchmark(ad, 0,  8.58, 50)
#do_move_benchmark(ad, 11.81, 8.58, 50)

print("Disconnecting")

# Close serial port to AxiDraw
ad.disconnect()

print("Goodbye!")
