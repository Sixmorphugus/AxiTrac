from pyaxidraw import axidraw
import serial
import time
import threading

G_line = ""

# Returns the last serial message that was received, throwing out all ones that came before it.
def receive_serial_async():
    global G_line
    
    if ser.inWaiting() > 0:
        G_line = G_line + ser.read(ser.inWaiting()).decode("ascii")

    # strip all completed symbols off the start of line
    completed = G_line

    while len(completed) > 0 and completed[-1] != "|":
        completed = completed[:-1]

    G_line = G_line.replace(completed, "")
    lastOutput = "";
    
    try:
        lastOutput = completed.split("|")[-2]
    except ValueError:
       # happens sometimes, ignore
       pass
    except IndexError:
       # nothing was found in the buffer
       pass

    return lastOutput

def await_press(button):
    startTime = time.time()
    tolerence = 30.0
    
    while True:
        serialIn = receive_serial_async()

        if(serialIn != ""):
            serialInParts = serialIn.split("&")
            
            serialInPressure = int(serialInParts[button])

            if(serialInPressure > tolerence):
                return serialInPressure, time.time() - startTime

def poll_press(button):
    tolerence = 30.0

    serialIn = receive_serial_async()
    serialInPressure = 0

    if(serialIn != ""):
        serialInParts = serialIn.split("&")
        serialInPressure = int(serialInParts[button])

    return serialInPressure, serialInPressure > tolerence

def write_csv_row(file, row):
    for i in range(len(row)):
        if i != 0:
            file.write(",")

        file.write(str(row[i]))

    file.write("\n")

# connect to Arduino
ser = serial.Serial("COM4", 9600)

togOn = False

# Connect to AxiDraw
ad = axidraw.AxiDraw() 
ad.interactive()
ad.connect()

while True:
    while True:
        fileName = input("Enter test file to run: ")

        try:
            file = open(fileName, 'r')
            break
        except:
            print("Couldn't open that file for read.")
    

    outFile = open(fileName + "_result", 'w')

    # Experiment 1 format:
    # XPositionToMoveToAndStop, NumberOfMeasurementsToTake

    # Experiment 2 format:
    # XSpeedToMoveToEndAt, NumberOfMeasurementsToTake
    
    lines = file.readlines()

    for e in range(len(lines)):
        line = lines[e]
        values = line.split(",")

        if(len(values) != 3):
            print("Line", e, "is not a valid experiment, skipping")
            continue

        if(int(values[0]) == 1): # Experiment 1
            xPositionToMoveToAndStop = float(values[1])
            numberOfMeasurementsToTake = int(values[2])

            print("Experiment 1;", xPositionToMoveToAndStop, numberOfMeasurementsToTake)

            # Set axi's speed to something sensible
            ad.options.speed_penup = 100
            ad.options.speed_pendown = 100
            ad.options.const_speed = True
            ad.options.accel = 100
            ad.update()

            for i in range(numberOfMeasurementsToTake):
                # Await press of button A
                recordedPressureForStart, timeToStart = await_press(0)

                print("Start reading took", timeToStart, "pressure", recordedPressureForStart)

                # Move axi to the configured position
                ad.goto(xPositionToMoveToAndStop, 0)

                # Await press of button B
                recordedPressureForStop, timeToStop = await_press(1)

                print("Finish reading took", timeToStop, "pressure", recordedPressureForStop)

                ad.goto(0, 0)

                # Record the result in outFile
                # Format: Experiment [1/2], Experiment Number [e], Reading Number [i], recordedPressureForStart, timeToStart, recordedPressureForStop, timeToStop
                row = [1, e, i, recordedPressureForStart, timeToStart, recordedPressureForStop, timeToStop]
                write_csv_row(outFile, row)
        if(int(values[0]) == 2): # Experiment 2
            xSpeed = float(values[1])
            numberOfMeasurementsToTake = int(values[2])

            print("Experiment 2;", xSpeed, numberOfMeasurementsToTake)

            for i in range(numberOfMeasurementsToTake):
                # Await press of button A
                recordedPressureForStart, timeToStart = await_press(0)

                print("Start reading took", timeToStart, "pressure", recordedPressureForStart)

                # Set axi's speed
                ad.options.speed_penup = 100
                ad.options.speed_pendown = xSpeed
                ad.options.const_speed = True
                ad.options.accel = 100
                ad.update()

                # lower the pen now so lowering it doesn't affect our time (part of the constant speed hack)
                ad.pendown() 

                # throw the experiment start time in here to avoid extra variable
                timeToStop = time.time()

                # Now move axi all the way to the end at this speed and back, ""asynchronously""
                # This involves two for loops which cause the axi to make very small "steps" up and down the x axis at a constant speed.
                # The constant speed is why the pen needs to remain down.
                steps = 20
                buttonHit = False

                while True:
                    for j in range(steps):
                        ad.lineto((11.81 / steps) * (j+1), 0)

                        # Poll press of button B (don't wait for it, but record it)
                        recordedPressureForStop, overTol = poll_press(1)

                        if(overTol):
                            timeToStop = time.time() - timeToStop;
                            buttonHit = True
                            
                            break

                    if not buttonHit:
                        for j in range(steps, -1, -1):
                            ad.lineto((11.81 / steps) * j, 0)

                            # Poll press of button B (don't wait for it, but record it)
                            recordedPressureForStop, overTol = poll_press(1)
                            
                            if(overTol):
                                timeToStop = time.time() - timeToStop;
                                buttonHit = True

                                break
                            
                    if buttonHit:
                        break

                print("Finish reading took", timeToStop, "pressure", recordedPressureForStop)

                # Reset after 2 seconds
                time.sleep(1)
                
                # Move it back
                ad.moveto(0, 0)

                # Record the result in outFile
                # Format: Experiment [1/2], Experiment Number [e], Reading Number [i], recordedPressureForStart, timeToStart, recordedPressureForStop, timeToStop
                # Todo: figure out how to get position on the axis on touch earlier
                row = [2, e, i, recordedPressureForStart, timeToStart, recordedPressureForStop, timeToStop]
                write_csv_row(outFile, row)
        
    file.close()
    outFile.close()
