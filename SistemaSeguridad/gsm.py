#!/usr/bin/env python
import sys
import RPi.GPIO as GPIO
import time
import os
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(16, GPIO.OUT) ## GPIO 16 como salida, led OK, led verde del rpi
os.system("sudo echo none > /sys/class/leds/led0/trigger")
#print "Ejecucion iniciada..."
#GPIO.output(16,GPIO.HIGH)
filename=str(sys.argv[1]) 
complete_filename="/home/pi/inbox_sms/"+filename 
sms_file=open(complete_filename,"r") 
message=sms_file.read(160) #note that a not-parted SMS can be maximum 160 characters 
if (message.find("ON")<>-1): 
#	GPIO.output(16,GPIO.LOW) ## Enciendo el 17
	os.system("sudo echo 1 > /homebrightness")
elif (message.find("OFF")<>-1): 
#	GPIO.output(16,GPIO.HIGH) ## Apago el 17
	os.system("echo 0 > /sys/class/leds/led0/brightness")
#print "Ejecucion finalizada"

