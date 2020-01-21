from pyaxidraw import axidraw
import serial

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

    G_line = line.replace(completed, "")
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
    tolerence = 30.0;
    
    while True:
        serialIn = receive_serial_async()

        if(serialIn != ""):
            serialInParts = serialIn.split("&")
            
            serialInPressure = int(serialInParts[button]))

            if(serialInPressure > tolerence):
                return serialInPressure, time.time() - startTime

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

    # Experiment 0 format:
    # XPositionToMoveToAndStop, NumberOfMeasurementsToTake
    lines = file.readlines()

    for e in range(len(lines)):
        line = lines[e]
        values = line.split(",")

        if(len(values) == 2): # Experiment 0
            xPositionToMoveToAndStop = float(values[0])
            numberOfMeasurementsToTake = int(values[1])

            for i in range(numberOfMeasurementsToTake):
                # Await press of button A
                recordedPressureForStart, timeToStart = await_press("A")

                # Move axi to the configured position
                ad.goto(xPositionToMoveToAndStop, 0)

                # Await press of button B
                recordedPressureForStop, timeToStop = await_press("B")

                # Record the result in outFile
                # Format: Experiment Type [0/1], Experiment Number [e], Reading Number [i], recordedPressureForStart, timeToStart, recordedPressureForStop, timeToStop
                row = [0, e, i, recordedPressureForStart, timeToStart, recordedPressureForStop, timeToStop]
                write_csv_row(outFile, row)
        # TODO Experiment 1
        
    file.close()
