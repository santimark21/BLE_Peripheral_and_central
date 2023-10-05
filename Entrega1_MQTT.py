from os import statvfs
from time import sleep
import network
from mqtt import MQTTClient 
import machine 
import time
import json
import random
from micropython import const
# librerias del central
import bluetooth
import random
import struct
import time
import sys
from simpleBLE import BLECentral
from machine import deepsleep
from machine import reset
from machine import Pin

USERNAME = const('Oy47CyELMRwqGgIcBAAcBz0')
CLIENTID = const('Oy47CyELMRwqGgIcBAAcBz0')
PASS = const('Nx2N7hQcekjWxf97RKBCWPUH')
SERVER=const('mqtt3.thingspeak.com')
CHANNEL=const('2288679')


def showData(data):
    global done_flag
    print(data)
    msg='field1='+str(data)
    print(msg)
    client.publish(topic="channels/"+CHANNEL+"/publish", msg=msg) 
    done_flag=True
    if button_pin.value()==1:
        deepsleep(15000)

done_flag=False
BUTTON=0
button_pin = Pin(BUTTON, Pin.IN)


def free_flash():
  s = statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))

# https://api.thingspeak.com/update?api_key=JGM08DVSS7Z3IX1U&field2=0
def sub_cb(topic, msg):
    print(msg[0])   
    if msg[0]==48:
       led.value(0)
    elif msg[0]==49:
        led.value(1)

print('Available flash memory: '+free_flash())

# Bluetooth object
ble = bluetooth.BLE()
# Environmental service
service= "ed570147-da2a-4e1f-8ae4-a3e11e4c0eec"
# characteristic
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
attempts=0
while True:
    time.sleep_ms(100)
    if central.is_connected():
        break;
    else:
        attempts=attempts+1
        if attempts==100:
            reset()
            
print("Connected")


led=machine.Pin(2,machine.Pin.OUT)


client = MQTTClient(client_id=CLIENTID, server=SERVER,user=CLIENTID,password=PASS )
 

client.set_callback(sub_cb) 
client.connect()
client.subscribe(topic='channels/'+CHANNEL+'/subscribe/fields/field2')

counter=0;
T=30
while True:
  try:  
    central.on_notify(callback= lambda data :print('Notified') )

# Explicitly issue reads, using "print" as the callback.
#while central.is_connected():
    central.read(callback=lambda data: showData(data[0]))
    time.sleep_ms(1000)
  

    sleep(1)
    counter+=1
    client.check_msg();
  except OSError as e:
    print('Failed')