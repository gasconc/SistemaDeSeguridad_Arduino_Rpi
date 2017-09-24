#!/usr/bin/python
from lib_nrf24 import NRF24
import time
import RPi.GPIO as GPIO
import spidev

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pipes = [[0xe8, 0xe8, 0xf0, 0xf0, 0xe1], [0xf0, 0xf0, 0xf0, 0xf0, 0xe1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,25)
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x4c)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.openReadingPipe(1, pipes[1])
radio.openWritingPipe(pipes[0])

radio.printDetails() #Opcional
radio.powerUp()


mensaje1 = list("on")
while len(mensaje1) < 32:
	mensaje1.append(0)
	
mensaje2 = list("off")
while len(mensaje2) < 32:
	mensaje2.append(0)
	

while True:
	
	time.sleep(1)
	radio.write(mensaje1)
	print("On")
	time.sleep(1)
	radio.write(mensaje2)
	print("Off")
	


