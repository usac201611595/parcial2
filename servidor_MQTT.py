import paho.mqtt.client as mqtt
import logging
import time
import os 
from broker_MQTT_datos import * #Informacion de la conexion

LOG_FILENAME = 'mqtt.log'

CLIENTE_ACTIVO= "comandos/12/" #MGHP parte inicial del TOPIC donde se recibiran los alives de los cliente para determinar si estan activos
ACK=b"x05" #MGHP constaste para responder a los alives
#MGHP nombre del archivo que contiene a los usuarios
usuarios='topics_usuarios.txt' # MGHP variable que representa el archivo donde se tienen guardado los usuarios




#funcion que guarda la informacion recibida de los alives.
def recepcion(contenidom):
    print("si estoy en la funcion")
    la_info=contenidom
    logging.info(str(la_info))

    datos2=la_info.split(b'$')

    #for i in datos2:
    logging.info(datos2)
    client.publish("comandos/12/201611595",ACK, qos = 0, retain = False)





#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )


def on_publish(client, userdata, mid):#MGHP para confirmacion de publicacion exitosa
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)


#Callback que se ejecuta cuando nos conectamos al broker
def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")


#Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado

    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))#MGHP a que topic llego el mensaje
    logging.info("El contenido del mensaje es: " + str(msg.payload)) #MGHP cual es el contenido del mensaje

    if msg.topic=="comandos/12": #MGHP condicion para verificar si esta llegando un comando
        logging.info("estoy recibiendo un comando") #MGHP muestra que si estoy recibiendo un comando
        recepcion(msg.payload) #MGHP llamo a la funcion para poder partir la informacion

    
    #Y se almacena en el log 
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
    os.system(logCommand)


client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #MGHP cuando registra una conexion, ejecuta el codigo contenido en on_connect
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto


def llama_usuarios(): # MGHP funcion que se encarga de crear una lista para poder utilizar la informacion de los usuarios
    qos = 2
    datos=[]

    archivo = open(usuarios, 'r')
    for linea in archivo:
        registro=linea.split(',')
        registro[-1]=registro[-1].split('\n')[0]
        datos.append(registro)
    archivo.close()

    for i in datos:
        logging.info(i[:])

    #dentro de esta misma funcion nos subscribimos a los usuarios para poder recibir informacion
    logging.info("estamos subcritos a los siguiente topics: \n")
    for j in range(len(registro)):
        client.subscribe((CLIENTE_ACTIVO+str(registro[j]),qos))#MGHP subscripcion a cada unos de los usuarios que estan dentrso del archivo
        logging.info(str(j)+" " +CLIENTE_ACTIVO+str(registro[j]))


llama_usuarios() #MGHP llama a la funcion que extrae la informacion del documento donde estan los clientes
#Nos conectaremos a distintos topics:


#Subscripcion simple con tupla (topic,qos)
#client.subscribe(("comandos", qos))

#Subscripcion multiple con lista de tuplas


#MGHP subscripcion para poder recibir los alives de los clientes
#client.subscribe((CLIENTE_ACTIVO, qos))

client.loop_start() #se comporta como un hilo tipo demonio


try:
    while True:
        logging.info("esperando mensaje de algun cliente")
        time.sleep(20)


except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")