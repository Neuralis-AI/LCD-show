#!/bin/bash
#clear display
clear

#get dependencies
apt install -y python3-pil 
pip3 install adafruit-circuitpython-ssd1306
pip3 install adafruit-circuitpython-mcp230xx

#get healthy
wget https://raw.githubusercontent.com/Neuralis-AI/LCD-show/master/etc/health.py -O "/home/s360box/logs/health.py"

#remove old shit
rm -f /home/s360box/logs/check.py

#crontab fiddling stuff
crontab -l > mycron
#echo new cron into cron file
echo "@reboot sleep 30; /home/s360box/logs/check.py >/dev/null 2>&1" >> mycron
echo "* * * * * pgrep -f check.py || nohup /home/s360box/logs/check.py >/dev/null 2>&1"

#install new cron file
crontab mycron
rm mycron

#touch privates
touch /home/s360box/logs/internet-check
echo 1 > /home/s360box/logs/internet-check

#dominate submissive files
chmod 777 /home/s360box/logs/internet-check
chmod a+x /home/s360box/logs/health.py

#clear display
clear

#say goodbye
print("All done! Now pull the plug daddy... (♥_♥)")
