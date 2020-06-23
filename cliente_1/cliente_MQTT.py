import paho.mqtt.client as paho
import logging
import random
from broker_MQTT_datos import * #Informacion de la conexion
import binascii#GAMS
import os   # LARP para utilizar la consola, enviar comandos
import time # LARP libreria para definir nombre en formato timestamp UNIX (epoch) #Retardos

# LARP Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO,
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )
#class Negocia(object):
#    def __init__(self,topic,contenidom):#GAMS
#        self.topic=str(topic)#GAMS
#        self.contenidom = contenidom#GAMSs
                                    #)
#    def alive(self):
#        t1 = threading.Thread( target = self.s_alive,
#                                        daemon = True
#                                        )
#        t1.start()
#    def ACK(self):#GAMS
#        return self.recepcion()[0]==b'x05' and self.recepcion()[1].decode("utf-8")=="201611595" and self.topic=="comandos/12"#GAMS
def recepcion(topic,contenidom):
    logging.info("si estoy en la funcion")
    #MGHP aqui empezamos a partir la informacion
    la_info=contenidom
    eltopic=topic.split('/')

    #daT=Negocia(eltopic,datos2[0],datos2[1].decode("utf-8"))
    #logging.info(str(daT.ACK()))
    nombre = ''
    if eltopic[0]=="audio": # LARP condicion, si pertenece al topic audios, guarda el audio
        print("recibiendo audio")
        nombre = str(int(time.time())) + '.wav' #LARP nombre de archivo, hora actual, timestamp
        archivo = open( nombre , 'wb') #LARP apertura y creacion del archivo de audio
        archivo.write(la_info) # LARP Los bloques se van agregando al archivo

        t1 = threading.Thread(name = 'Reproduccion de fondo', #LARP creacion de hilo para reproduccion
                            target = hiloReproducion,
                            args = ((nombre, 31)),
                            daemon = True
                            )
        t1.start()
    else:
        datos2=la_info.split(b'$')
        print(datos2[0].decode("utf-8")+":"+datos2[1].decode("utf-8"))
        #logging.info("estoy recibiendo un alive de: " + str(datos2[1]))

def hiloReproducion(entrada, num): #LARP 'funcion del hilo Reproduccion de fondo'
    logging.info('Grabacion finalizada, inicia reproduccion') # LARP mensaje al finalizar
    os.system('aplay ' + entrada) #LARP ejecutar en consola con aplay
    time.sleep (num)

# LARP Funciones por defecto. Tiempo de espera entre lectura y envio de datos de sensores a broker (en segundos)

# LARP Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc):
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.info(connectionText)

# LARP Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid):
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

#--------------------------GAMS.----------------------------
def on_message(client, userdata, msg):
    #logging.info("El remitente: " + str(msg.topic))
    recepcion(msg.topic,msg.payload) #MGHP llamo a la funcion para poder partir la informacion

logging.info("Cliente MQTT con paho-mqtt") #Mensaje en consola
'''
Config. inicial del cliente MQTT
'''
client = paho.Client(clean_session=True) # LARP Nueva instancia de cliente
client.on_connect = on_connect # LARP Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish # LARP Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

#Loop principal: leer los datos de los sensores y enviarlos al broker en los topics adecuados cada cierto tiempo
#try:

def Subcribir():
#    client.subscribe([("usuario/12/201611595",0),("salas/12/2s23",0),("comandos/12/201611595",0),("comandos/12",0)])
    client.subscribe([("usuario/12/201602613",0),("salas/12/2s23",0),("audio/12/201602613",0)])
    client.loop_start()
    #while True:
def Send_comando(topicRoot,topicName,value):
    topic = str(topicRoot) + "/12/" + str(topicName.decode("utf-8"))
    client.publish(topic, value, qos = 0, retain = False)

#except KeyboardInterrupt:
    #logging.warning("Desconectando del broker MQTT...")

#finally:
    #client.disconnect()
    #logging.info("Se ha desconectado del broker. Saliendo...")
