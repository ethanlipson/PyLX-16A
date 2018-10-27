# PyLX-16A
Ethan Lipson

Revision 0.80, October 27, 2018

## Introduction
PyLX-16A is a Python library designed to control one or more of LewanSoul's LX-16A servos. This document will walk you through the different steps of using the library to control one or more servos.

The library has the following structure:
* There is a central `LX16A` class
* Each real-life servo has a corresponding instance of the `LX16A` class in the program
* The virtual servos have member functions that control the physical servos
* When there is an error relateing to a servo or servos, a `ServoError` exception is thrown

## Setup

To set up a system, such as a robot with multiple servos:
* Install the hardware, including the servos, a power supply, a servo controller board, and cables
* Create a folder containing lx16a.py, and your main program (such as the provided sample, helloWorld.py)
* Run the program (if you are running the sample program, the servos will oscillate in a sine wave out of phase with each other)

### Hardware Installation

To set up the hardwaere for the servos:
1. aaa
2. bbb
3. wah
