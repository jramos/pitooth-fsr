# pitooth-fsr

A stack which allows a force-sensitive resistor to act as a Bluetooth keyboard and send keystrokes when the resistor is depressed.

## Hardware

* 1 x [Pi cobbler](https://www.adafruit.com/products/2029)
* 1 x [FSR](https://www.adafruit.com/products/1071)
* 1 x 10k resistor
* 1 x LED (optional)

## Compiling & Installing Dependencies

### Bluetooth Keyboard Daemon

    cd btkbdd
    make
    sudo cp btkbdd /usr/local/bin

### keystroke

    g++ -o keystroke keystroke.c
    sudo cp keystroke /usr/local/bin

## Running

Start the Bluetooth keyboard daemon:

    sudo btkbdd /dev/input/event0 -d

Start the FSR listener:

    sudo ./fsr.py

## Usage

* Pair the Pi with another device as a keyboard (e.g. a mobile phone)
* When the FSR is depressed, an `s` key will be transmitted
* Respond to the keystroke on the paired device (e.g. start/stop a timer)
