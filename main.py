import threading #Concurrencia con hilos
import time      #Retardos
import sys
import logging#GAMS
#####GAMS BLOQUES NECESARIOS
import binascii#GAMS
from cliente_MQTT import *  #GAMS
from Cliente_pr12 import * ##GAMS importa los parametros de conexion
from control_cliente import *#GAMS


#def alive(delay):
#    while True:
#        Send_comando(C_ALIVE+USERID)
#        time.sleep(delay)
def s_alive(delay = 1):
    while True:
        Send_comando(comando,USERID,C_ALIVE+b'$'+USERID)
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




Subcribir()

cnt = 0
try:
    while True: #GAMS
    #------------------------tratamineto de mensajes -------------------------------------------
        N=input('\n enviar mensaje:"a", envia audio :"B" salir:"E" :')#GAMS
        if N=="a" or N=="A":#GAMS
            N=input('\n escbirir a usuario:"a", escribir sala:"b" :')#GAMS
            if N=="a":#GAMS
                N=input("\ncaré destino :")#GAMS
                data=input("Mensaje :")#GAMS
                Send_comando(user,N.encode("utf-8"),data)#GAMS
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
            elif N=="b":#GAMS
                N=input("No. sala :")#GAMS
                data=input("Mensaje :")#GAMS#GAMS
                Send_comando(user,N.encode("utf-8"),data)#GAMS
                logging.info('\n Enviando a: {!s}'.format(N))#GAMS
        elif N=="b" or N=="B":#GAMS
    #-------------------------tratamiento de audio-------------------------------------------
            N=input('\n desea enviar a usuario escriba "a" o sala escriba "b" :')#GAMS
            if N=="a":#GAMS
                N=input("\ncaré destino :")#GAMS
                data=input("tiempo a grabar(segundos) :")#GAMS
                Send_comando(comando,USERID,C_FTR+b'$'+N.encode("utf-8")+b'$'+b'120')#GAMS
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
            elif N=="b":#GAMS
                N=input("No. sala :")#GAMS
                data=input("tiempo a grabar(segundos) :")#GAMS
                Send_comando(comando,USERID,C_FTR+b'$'+N.encode("utf-8")+b'$'+b'120')#GAMS
                logging.info('\n Enviando a: {!s}'.format(N))#GAMS
        elif N=="e" or N=="E":#GAMS
            break#GAMS

except KeyboardInterrupt:

    logging.INFO("Terminando hilos")

    if t1.isAlive():
        t1._stop()

finally:
    sys.exit()
