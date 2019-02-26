# pitooth-fsr

Allows a force sensitive resistor to act as a Bluetooth keyboard and send a keystroke when depressed.

## Usage

* Pair Raspberry Pi with another device as a keyboard (e.g. a mobile phone)
* When the FSR is depressed, `s` will be transmitted
* Respond to the keystroke on the paired device (e.g. start/stop a timer)

## Hardware

* 1 x [Pi cobbler](https://www.adafruit.com/products/2029)
* 1 x [FSR](https://www.adafruit.com/products/1071)
* 1 x USB Bluetooth adapter
* 1 x 10k resistor
* 1 x LED (optional)

```
LED_PIN = 5
FSR_PIN = 25
```

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
