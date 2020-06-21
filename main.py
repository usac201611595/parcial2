import threading #Concurrencia con hilos
import time      #Retardos
import sys

import logging#GAMS
#####GAMS BLOQUES NECESARIOS
import binascii#GAMS
from cliente_MQTT import *  #GAMS
from Cliente_pr12 import * ##GAMS importa los parametros de conexion



#def alive(delay):
#    while True:
#        Send_comando(C_ALIVE+USERID)
#        time.sleep(delay)
def s_alive(delay = 1):
    while True:
        Send_comando(C_ALIVE+b'$'+USERID)
        time.sleep(delay) #Delay en segundos

logging.basicConfig(
    level = logging.DEBUG,
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

t1 = threading.Thread( target = s_alive,
                        args = (ALIVE_PERIOD, ),
                        daemon = True
                        )
t1.start()






cnt = 0
try:
    while True: #GAMS
    #------------------------tratamineto de mensajes -------------------------------------------
        N=input('\n Para enviar un mensaje escriba "A" para enviar a un audio escriba "B" para salir escriba "E" :')#GAMS
        if N=="a" or N=="A":#GAMS
            N=input('\n desea enviar a usuario escriba "a" o sala escriba "b" :')#GAMS
            if N=="a":#GAMS
                N=input("\n ingrese el numero de usuario :")#GAMS
                data=input("\ningrese su mensaje :")#GAMS
                logging.info('\n Enviando a: {!s}'.format(N))#GAMS
            elif N=="b":#GAMS
                N=input("\n"+b'ingrese el numero de sala :')#GAMS
                data=input("\ningrese su mensaje por favor :")#GAMS
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
        elif N=="b" or N=="B":#GAMS
    #-------------------------tratamiento de audio-------------------------------------------
            N=input('\n desea enviar a usuario escriba "a" o sala escriba "b" :')#GAMS
            if N=="a":#GAMS
                N=input("\ningrese el numero de usuario :")#GAMS
                data=input("cuanto tiempo desea grabar (segundos) :")#GAMS
                Send_comando(C_FTR+b'$'+N.encode("utf-8")+b'$'+b'120')#GAMS
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
            elif N=="b":#GAMS
                N=input("ingrese el numero de sala :")#GAMS
                data=input("\n cuanto tiempo desea grabar (segundos) :")#GAMS
                Send_comando(C_FTR+b'$'+N.encode("utf-8")+b'$'+b'120')#GAMS
                logging.info('\n Enviando a: {!s}'.format(N))#GAMS
        elif N=="e" or N=="E":#GAMS
            break#GAMS

except KeyboardInterrupt:

    logging.INFO("Terminando hilos")

    if t1.isAlive():
        t1._stop()

finally:
    sys.exit()
