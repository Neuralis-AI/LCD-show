#!/bin/bash
clear
apt install -y python3-pil 
pip3 install adafruit-circuitpython-ssd1306
pip3 install adafruit-circuitpython-mcp230xx

wget https://raw.githubusercontent.com/Neuralis-AI/LCD-show/master/etc/health.py -O "/home/s360box/logs/health.py"

touch /home/s360box/logs/internet-check
echo 1 > /home/s360box/logs/internet-check
chmod 777 /home/s360box/logs/internet-check
chmod a+x /home/s360box/logs/health.py
clear
print("All done! Now pull the plug daddy... (♥_♥)")
