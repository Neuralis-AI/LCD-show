#/usr/bin/env python3
import subprocess
import time
import requests
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
import os
from threading import Thread
import sys
from datetime import datetime

#init
#IO stuff
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)
pin1 = mcp.get_pin(1) #fysieke output 2
pin2 = mcp.get_pin(2) #fysieke output 3
pin4 = mcp.get_pin(4) # input 2
pin5 = mcp.get_pin(5) # input 3
pin1.switch_to_output(value=False)
pin2.switch_to_output(value=False)
pin1.value = False
pin2.value = False

#trigger
def trigger():
    print("trigger called")
    global i2c
    global mcp
    global pin1
    global pin2
    global pin4
    global pin5
    triggercheck = errordocker + errorcamera + errorinternet
    if pin4.value or pin5.value:
        pin2.value = True
        print("input 2 of 3 getriggered " + str(datetime.now()), file=open("triggerlog.txt", "a+"))
    else:
        pin2.value = False  
    if  triggercheck != 0:
        pin1.value = True
    else:
        pin1.value = False

        #errorstates
errordocker = 0
errorcamera = 0
errorinternet = 0

# docker stuff
watchlist = ["capture", "healthcheck", "alarmtrigger","azureiotedge-agent"]

while True:
    #dockercheck
    print("started dockercheck")
    for row in watchlist:
            stat = subprocess.check_output('docker ps', shell=True).decode("utf-8")
            if row not in stat:
                errordocker = 1
                trigger()
                time.sleep(1)
                print("dockerloop " + str(datetime.now()), file=open("triggerlog.txt", "a+"))
            else:
                errordocker = 0
                trigger()
                time.sleep(1)
    #cameracheck
    print("started cameracheck")
    dvars = f = open("camera-ping-result", "r")
    if "0" in dvars:
        errorcamera = 1
        print("cameraloop " + str(datetime.now()), file=open("triggerlog.txt", "a+"))
        trigger()
    elif "1" in dvars:
        errorcamera = 0 
        trigger()
    #internetcheck 
    print("started internetcheck")
    try:
        #eventueel al aanpassen naar https?
        response = requests.get("https://www.google.com")
        if "200" in str(response):
            errorinternet = 0
            print("1", file=open("internet-check", "w"))
            trigger()
        else:
            errorinternet = 1
            print("internetloop " + str(datetime.now()), file=open("triggerlog.txt", "a+"))
            print("0", file=open("internet-check", "w"))
            trigger()
            time.sleep(1)
    except requests.ConnectionError:
            errorinternet = 1
