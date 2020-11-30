#!/bin/bash
apt install -y python3-pil 
pip3 install adafruit-circuitpython-ssd1306
pip3 install adafruit-circuitpython-mcp230xx

wget "health.pyurl" -O "/home/s360box/logs/health.py"
chmod a+x /home/s360box/logs/health.py

print("All done! Now pull the plug daddy... 👁️👅👁️")
