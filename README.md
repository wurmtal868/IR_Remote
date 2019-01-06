# IR-Remote

This repository describes how to use an Arduino with an ATmega32U4 as an IR receiver for a HTPC running Linux.

See YouTube for the built video:

[![](http://img.youtube.com/vi/LgeRr3wnThw/0.jpg)](http://www.youtube.com/watch?v=LgeRr3wnThw "")

The MCU FW decodes the IR signal and sends the HEX code of the command to the USB serial connection.
If it can't detect the serial connection, it will assume that the PC is in power off and will activate a relay when power button on the remote gets pushed.

The current FW is programed to recognize the power button of a TechnoTrend IR remote that uses an RC5 encoding.
It can easily be adjusted to any other IR remote that is supported by the Arduino IR remote library.

I used a clone of the Sparkfun Pro-Micro : https://www.sparkfun.com/products/12640

Required Arduino Libraries: https://github.com/z3t0/Arduino-IRremote

To run the Python scripts you need the program XTE to be installed. On Ubuntu based systems you find it in the package "xautomation"
