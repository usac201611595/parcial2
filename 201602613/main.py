import threading #Concurrencia con hilos
import time      #Retardos
import sys
import logging
import os
import binascii#GAMS
#####GAMS BLOQUES NECESARIOS creados en arcvos python
from cliente_MQTT_clases import *  #GAMS importmaos la clases de cliente
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

def GrabadrAudio(time,receptor):#GAMS funcion para grabar y enviar audo
    logging.info('Comenzando grabacion')#GAMS informacion que esta grabando
    os.system('arecord -d '+str(time)+' -f U8 -r 8000 temporal.wav')#GAMS ejecuta la instrucion para grabar audio donde time es el tiempo a grabar
    with open('temporal.wav', 'rb') as f:  #GAMS Se abre el archivo a enviar en BINARIO
        logging.info("enviando grabacion")#GAMS indica que el audio se va a enviar
        de=f.read()#GAMS guarda los binarios en la variable de
        usuario.Send_comando(audio,receptor.encode("utf-8"),de)#GAMS envia la grabacion  al receptor
        logging.info("grabacion enviada")#GAMS indica que se a enviado satisfactoriamente
        f.close()#GAMS cieera el archivo

temporal = str(usuario.user_id[0])
USERID = temporal.encode("utf-8")

cnt = 0
try:

    while True: #GAMS inicia un bucle para que el menu sea el hilo principal
        time.sleep(1)
    #------------------------tratamineto de mensajes -------------------------------------------
        N=input('\nSi desea enviar mensaje escriba : "a" \nSi desea enviar audio escriba: "b" \nSi desea salir escriba:"E" : \n')#GAMS pregunta al usuario que desea hacer
        if N=="a" or N=="A":#GAMS si es a enviara  un mensaje
            N=input('\nSi desea escribir a usuario coloque:"a" \nSi desea escribir a sala coloque:"b" : \n')#GAMS pregunta a quien o a quienes deseea enviar
            if N=="a" or N == "A" : #GAMS si es a envia a un usuario
                N=input("\nEscriba Usuario de destino (Ejemplo: 201112345): ")#GAMS pregunta a que usuario desea enviar
                data=input("Mensaje: ")#GAMS pergunta el cuerpo del mensaje
                usuario.Send_comando(user,N.encode("utf-8"),USERID.decode("utf-8")+"$"+data)#GAMS manda el mensaje y un id para identificar quien es el remitente
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS se informa que a sido enviado satisfactoriamente
            elif N=="b" or N == "B":#GAMS si es b  a seleccionado una sala
                N=input("Escriba No. de sala (Ejemplo : 01-99): ")#GAMS pregunta a que numero de sala desea enviar
                b="12S"+N#GAMS ayuda a que el usuario solamente ingrese el numero de sala
                data=input("Escriba el mensaje que desea enviar: ")#GAMS pregunta el cuerpo del mensaje
                usuario.Send_comando(salaxx, b.encode("utf-8"), USERID.decode("utf-8")+"$"+data)#GAMS  manda el mensaje
                logging.info('\nEnviando a sala: {!s}'.format(N))#GAMS informa que el mensaje a sido enviado
            else:#GAMS si el usuario ingreso una condicion no valida
                logging.warning('El valor ingresado no es valido')#GAMS le informa al usuario que su opcion no es valida
        elif N=="b" or N=="B":#GAMS si es b se enviara un archivo de audio
    #-------------------------tratamiento de audio-------------------------------------------
            N=input('\nSi desea enviar a usuario escriba "a" \nSi desea enviar a sala escriba "b": ')#GAMS pregunta a quien desea enviar
            if N=="a" or N=="A":#GAMS si es a lo enviara a un usario
                N=input("\nEscriba Usuario de destino (Ejemplo: 201112345): ")#GAMS pregunta el numero del usuarios
                data=input("Ingrese el tiempo a grabar (maximo 30 segundos): ")#GAMS indica al usuario cuanto tiempo deseea grabar
                usuario.Send_comando(user,N.encode("utf-8"),USERID.decode("utf-8")+"$"+'Recibiendo audio...')#GAMS le informa al usuario o sala que van a enviar un audio
                GrabadrAudio(data,N)#GAMS manda los parametros a la funcion audio
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS indica que se a enviado el audio
            elif N=="b" or N=="B":#GAMS si selecciono b manda el audio a la sala b
                N=input("Escriba No. de sala (Ejemplo : 01-99): ")#GAMS pregunta a que sala se enviara
                b="12S"+N#GAMS ayuda a que el cliente solo seleccione un numero
                data=input("Ingrese el tiempo a grabar (maximo 30 segundos): ")#GAMS  pide un cuanto tiempo desea grabar
                usuario.Send_comando(salaxx,b.encode("utf-8") ,USERID.decode("utf-8")+"$"+'Recibiendo audio...')#GAMS informa a la sala que se enviara un aduio
                GrabadrAudio(data,b)#manda inicia la grabacion y la envia
                logging.info('\nEnviando a: {!s}'.format(N))#GAMS informa que se a enviado el audio
            else:#GAMS si el cliente selecciono una opcion invalida le informa a este
                logging.warning('El valor ingresado no es valido')#GAMS indica que el valor no a sido valido
        elif N=="e" or N=="E":#GAMS para teriminar la secion
            break#GAMS para salir del while
        else:#GAMS si el usuario ingreso un valor no valido
            logging.warning('El valor ingresado no es valido')#GAMS le indica al usuario que este no es valido

except KeyboardInterrupt:

    logging.info("Terminando hilos")

finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker. Saliendo...")
    sys.exit()
