#!/usr/bin/env python
# Ejemplo de como enviar SMS usando gammu y python

import gammu
import sys

# crea un objeto stateMachine, para hablar con el telefono
sm = gammu.StateMachine()

# Leer la configuracion desde (~/.gammurc)
sm.ReadConfig()

# Iniciamos la conexión con el telefono
sm.Init()

# Preparamos el paquete de mensaje SMS
# SMSC es un numero que se puede obtener interrogando el telefono
message = {
 'Text': 'test SMS',
 'SMSC': {'Location': +584264568828},
 'Number': '+584264568828',
}

# Enviar el mensaje
sm.SendSMS(message)