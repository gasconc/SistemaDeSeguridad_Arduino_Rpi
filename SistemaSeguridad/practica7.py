from lib_nrf24 import NRF24
import time
import RPi.GPIO as GPIO
import spidev as SPI
import gammu 

sm = gammu.StateMachine()
sm.ReadConfig()
sm.Init()

armada = False
band = True
mensajeOK = ""
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

##########################################################################
def leerTxt():
	global mensajeOK
	archi=open('/sys/class/leds/led0/trigger','r')
	mensajeOK = archi.readline()
	archi.close()

##########################################################################
def armarAlarma(channel):
	global armada
	global band
	band = True
	if(armada == False):
		radio.write(mensaje1)
		print("On")
	elif(armada == True):
		radio.stopListening
		print("Off")

	armada = not armada

###########################################################################
pipes = [[0xe8, 0xe8, 0xf0, 0xf0, 0xe1], [0xf0, 0xf0, 0xf0, 0xf0, 0xe1]]

radio = NRF24(GPIO, SPI.SpiDev())
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
###############################################################################

while True:
	print("Alarma Inactiva")
	time.sleep(1)
	radio.write(mensaje2)

	leerTxt()
	if mensajeOK == "255":
		armarAlarma()

	while (armada == True):
		if(band):
			radio.startListening()
			band = False

		while not radio.available(pipes[1]) and armada == True:
			time.sleep(1)
			print("Alarma Activa")

		mensaje = []
		radio.read(mensaje)
		string = ""

		for n in mensaje:
			if (n >= 32 and n <= 126):
				string += chr(n)

		if(string == "a"):
			print("Se activo la zona A")
			time.sleep(3)
		elif(string == "b"):
			print("Se activo la zona B")
			time.sleep(3)

		leerTxt()
		if mensajeOK == "0":
			armarAlarma()
