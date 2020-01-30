#Setup

#Running Experiments

#About the Programs

#About the AxiDraw
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