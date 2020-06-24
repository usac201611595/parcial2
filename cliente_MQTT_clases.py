import paho.mqtt.client as paho
import logging
import random
from broker_MQTT_datos import * #Informacion de la conexion
import binascii #GAMS
import os   # LARP para utilizar la consola, enviar comandos
import time # LARP libreria para definir nombre en formato timestamp UNIX (epoch) #Retardos

TOPICS_AUDIO= "audio/20/" #MGHP parte inicial del TOPIC donde se recibiran los audios
TOPICS_CHAT="usuario/12/"
#MGHP nombre del archivo que contiene a los usuarios
usuarios='usuarios.txt' # MGHP variable que representa el archivo donde se tienen guardado los usuarios
salas='salas.txt'

# LARP Configuracion inicial de logging
logging.basicConfig(    
    level = logging.DEBUG,
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

class clienteMQTT(object): # LARP clase de cliente mqtt

    # LARP que valores de inicio ? CONSTANTES: USER ID, LISTA DE LAS SALAS A LAS QUE PERTENECE, UNA LISTA DE OTROS USUARIOS 
                                                                                            # (puede publicar a cualquiera)
    def __init__(self): # LARP valores de entrada que no cambiaran y seran globales
        a = []
        a.append(self.leerArchivos('usuario.txt')) # LARP tu usario
        self.user_id = a[0] # LARP como devuelve una lista, solo tomo el string de adentro
        self.lista_sala = self.leerArchivos('salas.txt') # LARP la lista de salas
        self.lista_usuarios = self.leerArchivos('usuarios.txt') # LARP la lista de usuarios
    
    def leerArchivos(self, archivo1):
        datos = []
        archivo = open( archivo1, 'r') #MGHP abrimos el archivo que contiene la informacion de usuarios o salas
        for linea in archivo:
            registro=linea.split(',')
            registro[-1]=registro[-1].split('\n')[0]
            datos.append(registro)
        archivo.close()
        return datos[0]
    
    def recepcion(self, topic,contenidom):
        logging.debug("Si estoy en la funcion")
        #MGHP aqui empezamos a partir la informacion
        la_info=contenidom
        eltopic=topic.split('/')

        #daT=Negocia(eltopic,datos2[0],datos2[1].decode("utf-8"))
        #logging.info(str(daT.ACK()))
        nombre = '' # LARP variable nombre, definida afuera para que entre en la tupla del hilo
        if eltopic[0]=="audio": # LARP condicion, si pertenece al topic audios, guarda el audio
            print("recibiendo auido")
            nombre = str(int(time.time())) + '.wav' #LARP nombre de archivo, hora actual, timestamp
            archivo = open(nombre, 'wb') #LARP apertura y creacion del archivo de audio
            archivo.write(la_info) # LARP Los bloques se van agregando al archivo
            t1 = threading.Thread(name = 'Reproduccion de fondo', #LARP creacion de hilo para reproduccion
                                target = clienteMQTT.hiloReproducion,
                                args = ((nombre, 31)),
                                daemon = True
                                )
            t1.start() # LARP inicializacion del hilo
        else:
            datos2=la_info.split(b'$')
            print(datos2[0].decode("utf-8")+":"+datos2[1].decode("utf-8"))

    def hiloReproducion(self, entrada, num): #LARP 'funcion del hilo Reproduccion de fondo'
        logging.info('Grabacion finalizada, inicia reproduccion') # LARP mensaje al finalizar
        os.system('aplay ' + entrada) #LARP ejecutar en consola con aplay
        time.sleep (num)
    
    
    #Loop principal: leer los datos de los sensores y enviarlos al broker en los topics adecuados cada cierto tiempo
    #try:
    
    def llama_subscripciones(self, topicsss,contenidos): # MGHP funcion que se encarga de crear una lista para poder utilizar la informacion de los usuarios
        qos = 2
        datos=[]
        topicsss
        """ archivo = open(contenidos, 'r') #MGHP abrimos el archivo que contiene la informacion de usuarios o salas
        for linea in archivo:
            registro=linea.split(',')
            registro[-1]=registro[-1].split('\n')[0]
            datos.append(registro)
        archivo.close()"""
        if contenidos == 'usuarios.txt':
            self.subscribirVar( topicsss, self.lista_usuarios)
        elif contenidos == 'salas.txt':
            self.subscribirVar( topicsss, self.lista_sala)

    def subscribirVar(self, topic1, userSala):
        #MGHP dentro de esta misma funcion nos subscribimos a los usuarios para poder recibir informacion
        for j in range(len(userSala)):
            client.subscribe((topic1+str(userSala[j]),qos))#MGHP subscripcion a cada unos de los usuarios que estan dentrso del archivo
            client.loop_start()
            logging.info(topic1+str(userSala[j]))# MGHP mostramos a que topics estamos susbcritos de los clientes

    # LARP funcion llamada desde afuera proveniente de la clase cliente MQTT para publicar
    def Send_comando(self, topicRoot,topicName,value):
        topic = str(topicRoot) + "/12/" + str(topicName.decode("utf-8"))
        client.publish(topic, value, qos = 0, retain = False)

class tiempoInvalido(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return str("El tiempo debe ser menor a 31 segundos y almenos 1 segundo")

    def __repr__(self):
        return self.__str__()

class noPertenecesAsala(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return str("No perteneces a esa sala")

    def __repr__(self):
        return self.__str__()

""" ==================================# LARP por defecto MQTT =================================== """
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
    clienteMQTT.recepcion(msg.topic,msg.payload) #MGHP llamo a la funcion para poder partir la informacion

""" ================================== #LARP por defecto MQTT =================================== """

logging.info("Cliente MQTT con paho-mqtt") #Mensaje en consola

''' #LARP Config. inicial del cliente MQTT '''

client = paho.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto


logging.info("subscribiendo a topics: ")
logging.info("PARA AUDIO: ")
#llama a la funcion que extrae la informacion de los documentos que contienen las salas y usuarios
clienteMQTT.llama_subscripciones(TOPICS_AUDIO,usuarios) #MGHP se subscribe a rececpion de audios de usuarios
clienteMQTT.llama_subscripciones(TOPICS_AUDIO,salas) #MGHP se subcribe recepcion de audios en salas
logging.info("PARA CHAT: ")
clienteMQTT.llama_subscripciones(TOPICS_CHAT,usuarios)#MGHP se subscribe a recepcion de chats en usuarios
clienteMQTT.llama_subscripciones(TOPICS_CHAT,salas)#MGHP se subscribe a recepcion de chats en salas.

logging.info("subscripcion exitosa")
client.loop_start()

#except KeyboardInterrupt:
    #logging.warning("Desconectando del broker MQTT...")

#finally:
    #client.disconnect()
    #logging.info("Se ha desconectado del broker. Saliendo...")