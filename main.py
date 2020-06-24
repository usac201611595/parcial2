import threading #Concurrencia con hilos
import time      #Retardos
import sys
import logging#GAMS
import os
#####GAMS BLOQUES NECESARIOS
import binascii#GAMS
from cliente_MQTT_clases import *  #GAMS
from Cliente_pr12 import * ##GAMS importa los parametros de conexion

usuario = clienteMQTT()

usuario.llama_subscripciones(TOPICS_AUDIO,salas) #MGHP se subcribe recepcion de audios en salas
usuario.llama_subscripciones(TOPICS_AUDIO,usuarios) #MGHP se subscribe a rececpion de audios de usuarios
logging.info("PARA CHAT: ")
usuario.llama_subscripciones(TOPICS_CHAT,usuarios)#MGHP se subscribe a recepcion de chats en usuarios
usuario.llama_subscripciones(TOPICS_SALA,salas)#MGHP se subscribe a recepcion de chats en salas.
logging.info("subscripcion exitosa")
client.loop_start()
logging.basicConfig(
    level = logging.INFO,
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

def GrabadrAudio(time,receptor):#GAMS
    logging.info('Comenzando grabacion')#GAMS
    os.system('arecord -d '+str(time)+' -f U8 -r 8000 temporal.wav')
    with open('temporal.wav', 'rb') as f:  #Se abre el archivo a enviar en BINARIO
        logging.info("enviando grabacion")#GAMS
        de=f.read()#GAMS
        #print(de)
        usuario.Send_comando(audio,receptor.encode("utf-8"),de)#GAMS
        logging.info("grabacion enviada")#GAMS
        f.close()#GAMS

temporal = str(usuario.user_id[0])
USERID = temporal.encode("utf-8")

cnt = 0
try:
    
    while True: #GAMS
        time.sleep(1)
    #------------------------tratamineto de mensajes -------------------------------------------
        N=input('\nSi desea enviar mensaje escriba : "a" \nSi desea enviar audio escriba: "b" \nSi desea salir escriba:"E" : \n')#GAMS
        if N=="a" or N=="A":#GAMS
            N=input('\nSi desea escribir a usuario coloque:"a" \nSi desea escribir a sala coloque:"b" : \n')#GAMS
            if N=="a" or N == "A" : #GAMS
                N=input("\nEscriba Usuario de destino (Ejemplo: 201112345): ")#GAMS
                data=input("Mensaje: ")#GAMS
                usuario.Send_comando(user,N.encode("utf-8"),USERID.decode("utf-8")+"$"+data)#GAMS
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
            elif N=="b" or N == "B":#GAMS
                N=input("Escriba No. de sala (Ejemplo : 01-99): ")#GAMS
                b="12S"+N
                data=input("Escriba el mensaje que desea enviar: ")#GAMS#GAMS
                usuario.Send_comando(salaxx, b.encode("utf-8"), USERID.decode("utf-8")+"$"+data)#GAMS
                logging.info('\nEnviando a sala: {!s}'.format(N))#GAMS
            else:
                logging.warning('El valor ingresado no es valido')
        elif N=="b" or N=="B":#GAMS
    #-------------------------tratamiento de audio-------------------------------------------
            N=input('\nSi desea enviar a usuario escriba "a" \nSi desea enviar a sala escriba "b": ')#GAMS
            if N=="a" or N=="A":#GAMS
                N=input("\nEscriba Usuario de destino (Ejemplo: 201112345): ")#GAMS
                data=input("Ingrese el tiempo a grabar (maximo 30 segundos): ")#GAMS
                usuario.Send_comando(user,N.encode("utf-8"),USERID.decode("utf-8")+"$"+'Recibiendo audio...')#GAMS
                GrabadrAudio(data,N)
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
            elif N=="b" or N=="B":#GAMS
                N=input("Escriba No. de sala (Ejemplo : 01-99): ")#GAMS
                b="12S"+N
                data=input("Ingrese el tiempo a grabar (maximo 30 segundos): ")#GAMS
                usuario.Send_comando(salaxx,b.encode("utf-8") ,USERID.decode("utf-8")+"$"+'Recibiendo audio...')#GAMS
                GrabadrAudio(data,b)
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
            else:
                logging.warning('El valor ingresado no es valido')
        elif N=="e" or N=="E":#GAMS
            break#GAMS
        else:
            logging.warning('El valor ingresado no es valido')

except KeyboardInterrupt:

    logging.info("Terminando hilos")

    if t1.isAlive():
        t1._stop()

finally:
    sys.exit()
