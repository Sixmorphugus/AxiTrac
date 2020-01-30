# Setup
## Physical Setup

## Breadboard Information

## Modifying PyAxiDraw to allow for faster speed

# Running Experiments
Experiments are run via selecting a `.csv` (Comma Seperated Values) configuration file with correctly formatted lines, where each line represents one experiment run repeatedly with the same parameters. The parameter format changes depending on the first value on each line, which selects which experiment to perform.

All experiments output values to the `.csv_result` file. The meaning of these readings varies depending on the selected experiment but all of them start with the experiment type, the experiment number, and the reading number.

## Fitt's Law Validation [1]
Fitt's Law Validation experiments always start with a 1 in their line in the CSV file. The format for a Fitts Law Validation experiment is therefore thus:
```1, [X Position To Move To], [No. Readings]```

The logic for running this experiment is that
- For the number of readings to take, repeatedly:
    - Wait for a press of button A, record pressure and time to hit in the results
    - Move to the position given in the configuration.
    - Wait for a press of B once movement has finished; record pressure and time to hit.
    - Record both readings in a new line in the `.csv_result` file.
    - Return to the home position.

The output format is:
```1, [Experiment Number], [Reading Number], [Recorded Pressure For Start], [Time Taken To Start], [Recorded Pressure For Stop, [Time Taken To Stop]```

## Moving Target [2]
Moving Target experiments always start with a 2 in their line in the CSV file. The format for a Moving Target experiment is therefore thus:
```2, [X Speed], [No. Readings]```

- For the number of readings to take, repeatedly:
    - Wait for a press of button A, record pressure and time to hit in the results
    - Begin moving back and forth at the speed specified in the configuration.
    - Wait for a press of B; record pressure and time to hit. Stop moving when touched.
    - Record both readings in a new line in the `.csv_result` file.
    - Return to the home position.

The output format is:
```2, [Experiment Number], [Reading Number], [Recorded Pressure For Start], [Time Taken To Start], [Recorded Pressure For Stop, [Time Taken To Stop, Approximate Axis Position On Touch]```

# About the Programs
## Auduino
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
- The AxiDraw stepper motors' maximum speed is only slightly higher than what the software allows by default: 25.
