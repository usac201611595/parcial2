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
    level = logging.DEBUG,
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

def GrabadrAudio(time,receptor):#GAMS
    logging.info('Comenzando grabacion')#GAMS
    os.system('arecord -d '+str(time)+' -f U8 -r 8000 201611595_server.wav')
    with open('201611595_server.wav', 'rb') as f:  #Se abre el archivo a enviar en BINARIO
        logging.info("enviando grabacion")#GAMS
        de=f.read()#GAMS
        #print(de)
        usuario.Send_comando(audio,receptor.encode("utf-8"),de)#GAMS
        logging.info("grabacion enviada")#GAMS
        f.close()#GAMS
cnt = 0
try:
    while True: #GAMS
    #------------------------tratamineto de mensajes -------------------------------------------
        N=input('\n enviar mensaje:"a", envia audio :"B" salir:"E" :')#GAMS
        if N=="a" or N=="A":#GAMS
            N=input('\n escbirir a usuario:"a", escribir sala:"b" :')#GAMS
            if N=="a":#GAMS
                N=input("\ncarné destino :")#GAMS
                data=input("Mensaje :")#GAMS
                usuario.Send_comando(user,N.encode("utf-8"),USERID.decode("utf-8")+"$"+data)#GAMS
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
            elif N=="b":#GAMS
                N=input("No. sala :")#GAMS
                b="12S"+N
                data=input("Mensaje :")#GAMS#GAMS
                print(b)
                usuario.Send_comando(salaxx, b.encode("utf-8"), USERID.decode("utf-8")+"$"+data)#GAMS
                logging.info('\n Enviando a: {!s}'.format(N))#GAMS
        elif N=="b" or N=="B":#GAMS
    #-------------------------tratamiento de audio-------------------------------------------
            N=input('\n desea enviar a usuario escriba "a" o sala escriba "b" :')#GAMS
            if N=="a":#GAMS
                N=input("\ncarné destino :")#GAMS
                data=input("tiempo a grabar(segundos) :")#GAMS
                usuario.Send_comando(user,N.encode("utf-8"),USERID.decode("utf-8")+"$"+data)#GAMS
                GrabadrAudio(data,N)
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
            if N=="b":#GAMS
                N=input("\n sala destino :")#GAMS
                b="12S"+N
                data=input("tiempo a grabar(segundos) :")#GAMS
                usuario.Send_comando(salaxx,b.encode("utf-8") ,USERID.decode("utf-8")+"$"+data)#GAMS
                print("pasa")
                GrabadrAudio(data,b)
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS
        elif N=="e" or N=="E":#GAMS
            break#GAMS

except KeyboardInterrupt:

    logging.info("Terminando hilos")

    if t1.isAlive():
        t1._stop()

finally:
    sys.exit()
