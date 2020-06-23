import threading #Concurrencia con hilos
import time      #Retardos
import sys
import logging#GAMS
#####GAMS BLOQUES NECESARIOS
import binascii#GAMS
from cliente_MQTT import *  #GAMS
from Cliente_pr12 import * ##GAMS importa los parametros de conexion
#from control_cliente import *#GAMS
#from Manejo_cliente import *


#def alive(delay):
#    while True:
#        Send_comando(C_ALIVE+USERID)
#        time.sleep(delay)
Subcribir()
#def s_alive(delay = 1):
#    while True:
#        #a.imprimir()
#        #Send_comando(comando,USERID,C_ALIVE+b'$'+USERID)
#        client.publish("comandos/12", C_ALIVE+b'$'+USERID, qos = 0, retain = False)#GAMS
#        time.sleep(delay) #GAMSDelay en segundos

logging.basicConfig(
    level = logging.DEBUG,
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

#ciclo_alive = threading.Thread( target = s_alive,
#                        args = (ALIVE_PERIOD, ),
#                        daemon = True
#                        )
#ciclo_alive.start()


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
                Send_comando(audio,N.encode("utf-8"),"enviando-audio")#GAMS
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
            elif N=="b":#GAMS
                N=input("No. sala :")#GAMS
                data=input("tiempo a grabar(segundos) :")#GAMS
                Send_comando(audio,N.encode("utf-8"),"enviando audio sala")#GAMS
                logging.info('\n Enviando a: {!s}'.format(N))#GAMS
        elif N=="e" or N=="E":#GAMS
            break#GAMS

except KeyboardInterrupt:

    logging.info("Terminando hilos")

    if t1.isAlive():
        t1._stop()

finally:
    sys.exit()
