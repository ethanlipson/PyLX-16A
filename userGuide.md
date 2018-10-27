# PyLX-16A
Created by Ethan Lipson

Revision 0.8.0, October 27, 2018

## Introduction
PyLX-16A is a Python library designed to control one or more of LewanSoul's LX-16A servos. This document will walk you through the different steps of using the library to control one or more servos.

The library has the following structure:
* There is a central `LX16A` class
* Each real-life servo has a corresponding instance of the `LX16A` class in the program
* The virtual servos have member functions that control the physical servos
* When there is an error relateing to a servo or servos, a `ServoError` exception is thrown

## Setup

To set up a system, such as a robot with multiple servos:
1. Install the hardware, including the servos, a power supply, a servo controller board, and cables
2. Create a folder containing lx16a.py, and your main program (such as the provided sample, helloWorld.py)
3. Run the program (if you are running the sample program, the servos will oscillate in a sine wave out of phase with each other)

### Hardware Installation

To set up the hardware for the servos:
1. Connect your compouter and the controller board with the provided USB cable
2. Connect a power source to the screw terminals on the controller board
3. Connect a servo to the controller board, it doesn't matter which socket you choose
4. (Optional) The servos can be daisy-chained, meaning you can connect servos to each other in sequence

At this point, I would recommend downloading LewanSoul's Bus Servo Terminal software, which will allow you to check if your hardware is set up correctly. It can be found under the PC Software tab on the Downloads section of [their website](https://lewansoul.com/).

### Software Installation

To add PyLX-!6A to your project, make sure you install pySerial (`pip install pyserial`), and then place `lx16a.py` into your project directory, or clone this GitHub repository.

Before controlling the servos, there is a bit of setup that must first be done.

#### Controller Board Initialization

sdgsfdg
dsfgdsfg
