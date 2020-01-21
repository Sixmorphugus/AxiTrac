import serial
from pyaxidraw import axidraw
import time

# connect to Arduino
ser = serial.Serial("COM4", 9600)

togOn = False

# Connect to AxiDraw
ad = axidraw.AxiDraw() 
ad.interactive()
ad.connect()

# Setup Axi a bit
ad.options.speed_penup = 110
ad.options.speed_pendown = 110
ad.options.accel = 100
ad.options.model = 1
ad.update()

line = ""

while True:
    if ser.inWaiting() > 0:
        line = line + ser.read(ser.inWaiting()).decode("ascii")

    # strip all completed symbols off the start of line
    completed = line

    while len(completed) > 0 and completed[-1] != "|":
        completed = completed[:-1]

    line = line.replace(completed, "")
    
    try:
        lastOutput = completed.split("|")[-2]
        pressure = int(lastOutput)

        if pressure > 10:
            if not togOn:
                print("pressed")
                togOn = True
        elif togOn:
            print("released")
            togOn = False

            ad.moveto(0, 0)
    except ValueError:
       # happens sometimes, ignore
       pass
    except IndexError:
       # nothing was found in the buffer
       pass

    if(togOn):
        ad.moveto((pressure / 100) * 3, 0)
