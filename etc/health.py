#/usr/bin/python3
import subprocess
import time
import requests
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
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
pin4 = mcp.get_pin(9) # input 2
pin5 = mcp.get_pin(10) # input 3
pin1.switch_to_output(value=False)
pin2.switch_to_output(value=False)
pin1.value = False
pin2.value = False

#display init stuff
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
disp.fill(0)
disp.show()
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
padding = -2
top = padding
bottom = height - padding
x = 0
font = ImageFont.load_default()

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
    try:
        sabotagecheck = subprocess.check_output("docker exec healthcheck env | grep SABOTAGE_DETECTION_DISABLED", shell=True).decode("utf-8")    
        if "=0" in sabotagecheck:
            if pin4.value or pin5.value:
                pin2.value = True
                print("input 2 of 3 getriggered " + str(datetime.now()), file=open("triggerlog.txt", "a+"))
            else:
                pin2.value = False
    except:
        if pin4.value or pin5.value:
            pin2.switch_to_output(value=True)
            print("input 2 of 3 getriggered " + str(datetime.now()), file=open("triggerlog.txt", "a+"))
        else:
            pin2.switch_to_output(value=False)
    if  triggercheck != 0:
        pin1.switch_to_output(value=True)
    else:
        pin1.switch_to_output(value=False)

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
    dvars = open("camera-ping-result", "r")
    for x in dvars:
        if "0" in x:
            errorcamera = 1
            print("cameraloop " + str(datetime.now()), file=open("triggerlog.txt", "a+"))
            trigger()
        elif "1" in x:
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
            #print naar display
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((x, top + 0), "Probleem ", font=font, fill=255)
            draw.text((x, top + 8), "met", font=font, fill=255)
            draw.text((x, top + 16), "internetverbinding", font=font, fill=255)
            draw.text((x, top + 24), "Volgende test: in 10 sec", font=font, fill=255)
            time.sleep(1)
    except requests.ConnectionError:
            errorinternet = 1
