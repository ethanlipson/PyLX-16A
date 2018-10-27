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
