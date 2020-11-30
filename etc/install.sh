#!/bin/bash
#clear display
clear

#get dependencies
apt install -y python3-pil 
pip3 install adafruit-circuitpython-ssd1306 adafruit-circuitpython-mcp230xx

#get healthy
wget https://raw.githubusercontent.com/Neuralis-AI/LCD-show/master/etc/health.py -O "/home/s360box/logs/health.py"

#remove old shit
rm -f /home/s360box/logs/check.py

#crontab fiddling stuff
crontab -l > mycron
#echo new cron into cron file
echo "@reboot /home/s360box/logs/health.py >/dev/null 2>&1" >> mycron
echo "* * * * * pgrep -f health.py || nohup /home/s360box/logs/health.py >/dev/null 2>&1" >> mycron
#install new cron file
crontab mycron
rm mycron

#touch privates
touch /home/s360box/logs/internet-check
echo 1 > /home/s360box/logs/internet-check
touch /home/s360box/logs/camera-ping-result

#dominate submissive files
chmod 777 /home/s360box/logs/internet-check
chmod a+x /home/s360box/logs/health.py
chmod 777 /home/s360box/logs/camera-ping-result

#clear display
clear

#say goodbye
echo "All done! Now pull the plug daddy... (♥_♥)"
