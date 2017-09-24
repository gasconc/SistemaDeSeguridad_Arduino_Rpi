from lib_nrf24 import NRF24 
import time 
import RPi.GPIO as GPIO 
import spidev as SPI 
import gammu
import sys

#crea un objeto stateMachine, para hablar con el telefono
sm = gammu.StateMachine()
#Leer la configuracion desde (-/.gammurc)
sm.ReadConfig()
#Iniciar la conexion por telefono
sm.Init()

pinOnOff = 15
armada = False
band = True
mensajeOK = ""
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Subprograma que escribe el sms dado al numero configurado
def escribirTxt(mensaje):
	message = {
		'Text':mensaje,
		'SMSC':{'Location': 1}, #ranura donde esta la sim.
		'Number':'+584123429330', #numero destino
	}
	sm.SendSMS(message)

#Subprograma que lee un archivo de texto.
def leerTxt():
	archi=open('/sys/class/leds/led0/brightness','r')
	mensajeOK = archi.read()
	archi.close()
	return mensajeOK

#Subprograma que habilita la alarma
#enviado una mensaje de on u off por el RF
def armarAlarma():
	global armada
	global band
	band = True
	if(armada == False):
		a = 0
		escribirTxt('Alarma Activada!')
		while a < 5:
			radio.write(mensaje1)
			print("On")
			a = a + 1
	elif(armada == True):
		escribirTxt('Alarma Desactivada!')
		radio.stopListening()
		print("Off")

	armada = not armada
	time.sleep(2)

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

while True:
	print("Alarma Inactiva")
	time.sleep(1)
	radio.write(mensaje2)
	
	if int(float(leerTxt())) == 255:
		armarAlarma()

	while (armada == True):
		if(band):
			radio.startListening()
			band = False
		print("Alarma Activa")
		time.sleep(1)

		while radio.available(pipes[1]):

			mensaje = []
			radio.read(mensaje)
			string = ""
			
			for n in mensaje:
				if (n >= 32 and n <= 126):
					string += chr(n)
			
			if(string == "a"):
				print("Se activo la zona A")
				escribirTxt('se activo la zona A')
			elif(string == "b"):
				print("Se activo la zona B")
				escribirTxt('se activo la zona B')
			time.sleep(5)
			string = ""
	
		if int(float(leerTxt())) == 0:
			armarAlarma()
