# This example finds and connects to a BLE temperature sensor (e.g. the one in ble_temperature.py).

import bluetooth
import random
import struct
import time
import sys
from simpleBLE import BLECentral
from machine import deepsleep

# Bluetooth object
ble = bluetooth.BLE()

# Environmental service
service= "ed570147-da2a-4e1f-8ae4-a3e11e4c0eec"

# Temperature characteristic
characteristic="e17d00c6-9212-4bf4-b3fa-cda696999862"

# BLE Central object
central = BLECentral(ble,service,characteristic)

not_found = False

def on_scan(addr_type, addr, name):
    if addr_type is not None:
        print("Found sensor:", addr_type, addr, name)
        central.connect()
    else:
        global not_found
        not_found = True
        print("No sensor found.")

central.scan(callback=on_scan)

# Wait for connection...
while not central.is_connected():
    time.sleep_ms(100)
    if not_found:
        sys.exit()

print("Connected")

central.on_notify(callback= lambda data :print('Notified') )

# Explicitly issue reads, using "print" as the callback.
while central.is_connected():
    central.read(callback=lambda data: print(data[0]/3600000))
    time.sleep_ms(1000)
    print('esta es la potencia compae, a mimir')
    #sleep for 1 second (1000 milliseconds)
    deepsleep(1000)

# Alternative to the above, just show the most recently notified value.
# while central.is_connected():
#     print(central.value())
#     time.sleep_ms(2000)

print("Disconnected")


