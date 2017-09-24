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

#radio.printDetails() #Opcional
radio.powerUp()
radio.startListening()

while True:
        while not radio.available(pipes[0]):
                time.sleep(1/100)
                pass

        mensaje = []
        radio.read(mensaje)
        #print("mensaje recibido: {}".format(mensaje))

        #print("traduciendo el mensaje a caracteres unicode..")
        string = ""

        for n in mensaje:
                if (n >= 32 and n <= 126):
                        string += chr(n)
        print("{}".format(string))






