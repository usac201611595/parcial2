import paho.mqtt.client as paho
import logging
import random
from broker_MQTT_datos import * #Informacion de la conexion
'''
Ejemplo de cliente MQTT: gateway de red de sensores
'''
#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO,
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )



#Tiempo de espera entre lectura y envio de dato de sensores a broker (en segundos)


#Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc):
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.info(connectionText)

#Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid):
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

#--------------------------GAMS.----------------------------
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    print("Ha llegado el mensaje al topic: " + str(msg.topic))
    print("El contenido del mensaje es: " + str(msg.payload))

    #Y se almacena en el log
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
    os.system(logCommand)
#-------------------------------

logging.info("Cliente MQTT con paho-mqtt") #Mensaje en consola
'''
Config. inicial del cliente MQTT
'''
client = paho.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

#Loop principal: leer los datos de los sensores y enviarlos al broker en los topics adecuados cada cierto tiempo
#try:
def Subcribir(Id):
    client.subscribe("comandos/12"+Id, 0)
    client.loop_start()
    #while True:
def Send_comando(comando):
    client.publish("comandos/12",comando, qos = 0, retain = False)#aqui se coloca a donde se quiere enviar el mensaje y e mensaje

#except KeyboardInterrupt:
    #logging.warning("Desconectando del broker MQTT...")

#finally:
    #client.disconnect()
    #logging.info("Se ha desconectado del broker. Saliendo...")
