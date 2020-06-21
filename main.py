
import logging
#####GAMS BLOQUES NECESARIOS
import binascii#GAMS
from cliente_MQTT import *  #GAMS
from Cliente_pr12 import * #importa los parametros de conexion

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(message)s'
    )
while True:
    N=input('\n Para enviar un mensaje escriba "A" para enviar a un audio escriba "B" para salir escriba "E" :')
    if N=="a" or N=="A":
        N=input('\n desea enviar a usuario escriba "a" o sala escriba "b" :')
        if N=="a":
            N=input("\n ingrese el numero de usuario :")
            data=input("\ningrese su mensaje :")
            logging.info('\n Enviando a: {!s}'.format(N))
        elif N=="b":
            N=input("\n ingrese el numero de sala :")
            data=input("\ningrese su mensaje por favor :")
            logging.info('\nEnviando a: {!s}'.format(N))
    elif N=="b" or N=="B":
#---------------------------audio-------------------------------------------
        N=input('\n desea enviar a usuario escriba "a" o sala escriba "b" :')
        if N=="a":
            N=input("\ningrese el numero de usuario :")
            data=input("cuanto tiempo desea grabar (segundos) :")
            Send_comando(C_FTR+USERID)
            logging.info('\nEnviando a: {!s}'.format(N))
        elif N=="b":
            N=input("\n ingrese el numero de sala :")
            data=input("\n cuanto tiempo desea grabar (segundos) :")
            Send_comando(C_FTR+USERID)
            logging.info('\n Enviando a: {!s}'.format(N))
    elif N=="e" or N=="E":
        break
