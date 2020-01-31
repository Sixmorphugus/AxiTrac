# Setup
## Software Setup
1. Install the core AxiDraw drivers: https://wiki.evilmadscientist.com/Axidraw_Software_Installation
2. Grab the PyAxiDraw software and drivers from here and follow the setup instructions: https://axidraw.com/doc/py_api/#about-axidraw
3. Grab the Auduino IDE: https://www.arduino.cc/en/main/software (Ideally don't get the new windows app)

## Physical Setup
1. Plug the AxiDraw into the wall (the stepper motors need mains power to run) and also into your own machine via micro USB.
2. Plug the Auduino into your own machine. It doesn't need mains power.
3. If any wires are disconnected, please refer to the Breadboard Information section for how everything should be plugged in. Also refer to this information if starting from scratch with a new AxiDraw, Breadboard and Auduino.

## Getting up and running
1. First of all, flash the Auduino with the Arduino program enclosed (main.ino). This gives us our indicator lights, and our pressure sensors.
2. Run the main.py file.

## Modifying PyAxiDraw to allow for faster speed
All speeds in the configuration file are relative to the maximum speeds the AxiDraw control software allows. Thus, you can allow faster speed by modifying PyAxiDraw's own files:
1. First you need to know where `pip` installed the Python library. It's always inside your Python directory, which is (usually) at `%LocalAppData%\Programs\Python\Python[Version]` on windows. The AppData folder is usually hidden from view on Windows, but typing the previous string into the address bar of the file manager usually works. Within this directory, go to `Lib\site-packages` (which is where `pip` usually puts its files) and open the `pyaxidraw` folder.
2. Open `axidraw_conf.py`. You will see a lot of settings.
3. The setting we want is near the end of the file, though you are welcome to adjust the others: it is `speed_lim_xy_hr`. Change this setting to `17.3958` (at most), and ignore the text telling you not to do that. We do not need the precision that this loses us; we are not drawing.
4. Run the program to check that it got faster.

## Advanced Physical Setup Information
The device should already be set up - this information covers how to create a new testbed.

### Parts
- 1x AxiDraw v3
- 1x Breadboard
- 1x Auduino
- 2x Pressure Sensor
- 9x LED (or 2, if you don't need indicators for testing the pressure sensors or speed)
- 2x pull-down resistor (One per pressure sensor, resistance of 4700 preferred)
- 1x Micro-USB cable (for Axi)
- 1x USB Type B cable (for Auduino)
- 1x Power Cable (for Axi)
- A lot of wires and sellotape

### Wiring Configuration
I will keep this vauge to allow for relatively free use of the breadboard. Thus, some previous experience of working with breadboards and switches is assumed.
1. Wire the first pressure sensor to A0. This will be button A.
2. Wire the second pressure sensor to A1. This will be button B.
3. Use pull-down resistors to make the sensors work (you can find guides on this elsewhere).
4. (Optional) If you want an indication of whether buttons A and B work, you can wire an LED to digital output 2 to test button A, and to digital output 3 to test button 4.
5. Wire 2 more LEDs to digital outputs 4 and 5. These will be our action indicator lights, A and B.
6. (Optional) If you want speed indication for the next experiment while evaluating moving targets, wire 5 more LEDs in a row to digital outputs 8-12. These are our speed indicator lights.

Ensure that everything is wired to ground where neccesary. I realise that telling an electronic engineer this is like telling a BASE jumper "Make sure to open your parachute before you hit the ground". You will probably be fine.

# Running Experiments
Experiments are run via selecting a `.csv` (Comma Seperated Values) configuration file with correctly formatted lines, where each line represents one experiment run repeatedly with the same parameters. The parameter format changes depending on the first value on each line, which selects which experiment to perform.

All experiments output values to the `.csv_result` file. The meaning of these readings varies depending on the selected experiment but all of them start with the experiment type, the experiment number, and the reading number.

## Fitt's Law Validation [1]
Fitt's Law Validation experiments always start with a 1 in their line in the CSV file. The format for a Fitts Law Validation experiment is therefore thus:
```1, [X Position To Move To], [No. Readings]```

The logic for running this experiment is that
- For the number of readings to take, repeatedly:
    - Wait for a press of button A (causing action light A to come on), record pressure and time to hit in the results
    - Move to the position given in the configuration.
    - Wait for a press of button B (causing action light B to come on) once movement has finished; record pressure and time to hit.
    - Record both readings in a new line in the `.csv_result` file.
    - Return to the home position.

The output format is:
```1, [Experiment Number], [Reading Number], [Recorded Pressure For Start], [Time Taken To Start], [Recorded Pressure For Stop, [Time Taken To Stop]```

## Moving Target [2]
Moving Target experiments always start with a 2 in their line in the CSV file. The format for a Moving Target experiment is therefore thus:
```2, [X Speed], [No. Readings]```

- For the number of readings to take, repeatedly:
    - Wait for a press of button A (causing action light A to come on), record pressure and time to hit in the results
    - Begin moving back and forth at the speed specified in the configuration.
    - Wait for a press of button B (causing action light B to come on); record pressure and time to hit. Stop moving when touched.
    - Record both readings in a new line in the `.csv_result` file.
    - Return to the home position.

The output format is:
```2, [Experiment Number], [Reading Number], [Recorded Pressure For Start], [Time Taken To Start], [Recorded Pressure For Stop, [Time Taken To Stop, Approximate Axis Position On Touch]```

# About the Programs
## Auduino
The Audrino program is very simple and establishes the first half of a very simple communication protocol. It does not control anything that the Axi is doing. Its job is:
- Send, over serial, a string containing:
    - A floating point number indicating the current pressure of button A.
    - An ampersand (&)
    - A floating point number indicating the current pressure of button B.
    - A pipe (|)
- Receive, over serial, and apply a single byte containing:
    - State for action light A (stored in the bit indicating "1")
    - State for action light B (stored in the bit indicating "2")
    
## AxiDraw

# About the AxiDraw
The API is quite simple to use and has a small number of functions.
- It has two modes: plot & interactive. I have been working in interactive mode as this is the mode that allows direct control of an AxiDraw device.
- The API allows you to change several options:
    - Move speed (when up/down); goes from 1 to 110, expressed as a percentage of the maximum speed which does not appear to be possible to change
    - Acceleration (time it takes to get up to speed)
    - Height the pen should be at when raised/lowered (this allows a small third axis of movement if you repeatedly change and update the options but this would be not nearly as well supported as the first two)
    - Delays and speeds for raising/lowering the pen
- Every time an API option is changed you must call update().
- The API functions to move pens all take a 2D vector to move to, but interpret it differently.
    - Three types of move; go, move, line
    - Two interpretations for each: relative, and to.
    - Full API: goto, moveto, lineto, go, move, line
    - Any function ending with “to” will move to an absolute position, otherwise the movement will be relative to where the “pen” is. All movements are clamped to the bounds of the working area.
    - go simply moves the pen; move moves with the pen up, and line moves with the pen down.
    - The existence of go implies you can manually raise and lower the pen. And you can; this is the purpose of penup and pendown.
- It takes approximately 2 seconds to move diagonally from the top left corner (“home” corner) of the working area to the bottom right
- The pen slot likely expects something a little heavier than the small piece of plastic that is in it at the moment, as the weight of this plastic piece is not enough for the pen to lower when the lifter component drops underneath its holder. If I had my own pen, I might try that, but it’s not a huge problem at the moment.
- The device needs to be started at the “home” position (0, 0) to work properly, otherwise it will be clamped to the wrong bounds and may grind when it tries to move outside of these. Thus, all programs should endeavour to return the device position to “home” before exiting.
- You cannot catch things such as KeyboardInterrupt while the device is in the middle of moving and give it new commands, as this messes with the internal state and will end up moving the “home” position to a random place. I did this earlier to try and make a constant movement state that I could stop and edit code on.
- If a program exits with the device in the wrong state, you will need to unplug it from your computer before physically resetting it to the correct position, as having it plugged into a machine with its driver installed locks it in place.
- If you accidentally send a bad command like move with 1 speed to the other side of the work area (which can take several minutes) you will need to unplug both the computer and power connection to reset the device. If you unplug only the computer, the device will continue running the command, and if you unplug only the device, the driver will resend the bad command as soon as power returns.
- The AxiDraw, contrary to what might seem to be happening, does NOT have any kind of motor in its moving segment. Both motors are either end of the device - one is X+Y, and one is X-Y. If you pull the driver belt in one direction on both sides of the moving segment, the head will move on the X axis. If you pull the driver belt in opposite directions, it will move on the Y axis.
- The AxiDraw stepper motors' maximum speed is only slightly higher than what the software allows by default: 25kHz.
