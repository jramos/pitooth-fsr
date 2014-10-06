#!/usr/bin/python2.7

import os
import sys
import bluetooth
from bluetooth import *
import dbus
import time

class Bluetooth:
    HOST = 0      # BT Mac address
    P_CTRL = 17   # control channel
    P_INTR = 19   # interrupt channel

    def __init__(self):
        # Set the device class to a keyboard, set the name, make discoverable
        os.system("hciconfig hci0 class 0x002540")
        os.system("hciconfig hci0 name PiToothFsr")
        os.system("hciconfig hci0 piscan")
        
        # Define our two server sockets for communication & bind to the ports
        self.scontrol = BluetoothSocket(L2CAP)
        self.scontrol.bind(("", Bluetooth.P_CTRL))
        self.sinterrupt = BluetoothSocket(L2CAP)
        self.sinterrupt.bind(("", Bluetooth.P_INTR))
        
        # Set up dbus for advertising the service record
        self.bus = dbus.SystemBus()
        try:
            self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/"), "org.bluez.Manager")
            adapter_path = self.manager.DefaultAdapter()
            self.service = dbus.Interface(self.bus.get_object("org.bluez", adapter_path), "org.bluez.Service")
        except:
            sys.exit("Could not configure bluetooth. Is bluetoothd started?")

        # Read the service record from file
        try:
            fh = open(sys.path[0] + "/sdp_record.xml", "r")
        except:
            sys.exit("Could not open the sdp record. Exiting...")

        self.service_record = fh.read()
        fh.close()

    def listen(self):
        # Advertise our service record
        self.service_handle = self.service.AddRecord(self.service_record)
        print "Service record added"

        # Start listening on the server sockets
        self.scontrol.listen(1) # Limit of 1 connection
        self.sinterrupt.listen(1)
        print "Waiting for a connection"
        self.ccontrol, self.cinfo = self.scontrol.accept()
        print "Got a connection on the control channel from " + self.cinfo[Bluetooth.HOST]
        self.cinterrupt, self.cinfo = self.sinterrupt.accept()
        print "Got a connection on the interrupt channel from " + self.cinfo[Bluetooth.HOST]

    def send_input(self, ir):
        #  Convert the hex array to a string
        hex_str = ""
        for element in ir:
          if type(element) is list:
            # This is our bit array - convrt it to a single byte represented as a char
            bin_str = ""
            for bit in element:
              bin_str += str(bit)
            hex_str += chr(int(bin_str, 2))
          else:
            # This is a hex value - we can convert it straight to a char
            hex_str += chr(element)
        # Send an input report
        self.cinterrupt.send(hex_str)

class Keyboard():
  def __init__(self):
    # The structure for an bt keyboard input report (size is 10 bytes)
    self.state = [
         0xA1, # This is an input report
         0x01, # Usage report = Keyboard
         # Bit array for Modifier keys
         [0,   # Right GUI - (usually the Windows key)
          0,   # Right ALT
          0,   # Right Shift
          0,   # Right Control
          0,   # Left GUI - (again, usually the Windows key)
          0,   # Left ALT
          0,   # Left Shift
          0],   # Left Control
         0x00,  # Vendor reserved
         0x00,  # Rest is space for 6 keys
         0x00,
         0x00,
         0x00,
         0x00,
         0x00 ]

  def event_loop(self, bt):
    while(1):
        print "sending state"
        bt.send_input(self.state)
        time.sleep(1)

# ----------------------------------------------------------

if __name__ == "__main__":
    # We can only run as root
    if not os.geteuid() == 0:
        sys.exit("Only root can run this script")

    bt = Bluetooth()
    bt.listen()
    kb = Keyboard()
    kb.event_loop(bt)
