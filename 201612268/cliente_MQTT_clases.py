import paho.mqtt.client as paho
import logging
import random
from broker_MQTT_datos import * #Informacion de la conexion
import binascii #GAMS para decodificar o codificar a binario
import os   # LARP para utilizar la consola, enviar comandos
import time # LARP libreria para definir nombre en formato timestamp UNIX (epoch) #Retardos
import threading

TOPICS_AUDIO= "audio/12/" #MGHP parte inicial del TOPIC donde se recibiran los audios
TOPICS_CHAT="usuario/12/"#MGHP nombre del archivo que contiene a los usuarios
TOPICS_SALA="salas/12/"#MGHP nombre del archivo que contiene a las salas

usuarios='usuario.txt' # MGHP variable que representa el archivo donde se tienen guardado los usuarios
salas='salas.txt'#MGHP variable que representa el archivo donde se tienen guardado las salas

# LARP Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO,
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
        self.lista_usuarios = self.leerArchivos('usuario.txt') # LARP la lista de usuarios

    def conseguirUser(self, num):
        return self.user_id

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
        nombre = '' # LARP variable nombre, definida afuera para que entre en la tupla del hilo
        if eltopic[0]=="audio": # LARP condicion, si pertenece al topic audios, guarda el audio
            print("recibiendo auido")
            nombre = str(int(time.time())) + '.wav' #LARP nombre de archivo, hora actual, timestamp
            archivo = open(nombre, 'wb') #LARP apertura y creacion del archivo de audio
            archivo.write(la_info) # LARP Los bloques se van agregando al archivo
            t1 = threading.Thread(name = 'Reproduccion de fondo', #LARP creacion de hilo para reproduccion
                                target = self.hiloReproducion,
                                args = ((nombre, 31)),
                                daemon = True
                                )
            t1.start() # LARP inicializacion del hilo
        elif eltopic[0]=="usuario":#GAMS si recibe de un usuario realiza lo siguiene
            datos2=la_info.split(b'$')#GAMS separamos la informacion
            print(datos2[0].decode("utf-8")+":"+datos2[1].decode("utf-8"))##GAMS decodificamos y desplegamos los valores seria quien lo mando y su mensaje
        elif eltopic[0]=="salas":#GAMS si fue sala relaza mostrara otro tipo de informacion
            datos2=la_info.split(b'$')#GAMS separamos la informacion para determinar el ID del remitente
            print("sala "+eltopic[2]+"----"+datos2[0].decode("utf-8")+":"+datos2[1].decode("utf-8"))##GAMS mostramos que sala y que usuario mando la informacion

    def hiloReproducion(self, entrada, num): #LARP 'funcion del hilo Reproduccion de fondo'
        logging.info('Grabacion finalizada, inicia reproduccion') # LARP mensaje al finalizar
        os.system('aplay ' + entrada) #LARP ejecutar en consola con aplay
        time.sleep (num)

    def llama_subscripciones(self, topicsss ,contenidos): # MGHP funcion que se encarga de crear una lista para poder utilizar la informacion de los usuarios
        datos=[]
        if contenidos == 'usuario.txt':
            self.subscribirVar( topicsss, self.lista_usuarios)
        elif contenidos == 'salas.txt':
            self.subscribirVar( topicsss, self.lista_sala)

    def subscribirVar(self, topic1, userSala):
        qos = 2
        #MGHP dentro de esta misma funcion nos subscribimos a los usuarios para poder recibir informacion
        for j in range(len(userSala)):
            client.subscribe((topic1+str(userSala[j]),qos))#MGHP subscripcion a cada unos de los usuarios que estan dentrso del archivo
            client.loop_start()
            logging.info(topic1+str(userSala[j]))# MGHP mostramos a que topics estamos susbcritos de los clientes

    # LARP funcion llamada desde afuera proveniente de la clase cliente MQTT para publicar
    def Send_comando(self, topicRoot,topicName,value):#GAMS funcion necesaria para mandar datos
        topic = str(topicRoot) + "/12/" + str(topicName.decode("utf-8"))#GAMS une el topicroot mas el topicName para formar un unico topic
        logging.debug(str(topic))#GAMS indica a que topic se enviara
        client.publish(topic, value, qos = 0, retain = False)#GAMS publica el mensaje en el topic

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
    logging.debug(connectionText)

# LARP Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid):
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

#--------------------------GAMS.----------------------------
def on_message(client, userdata, msg):
    usuario.recepcion(msg.topic,msg.payload) #MGHP llamo a la funcion para poder partir la informacion

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
usuario = clienteMQTT()


#except KeyboardInterrupt:
    #logging.warning("Desconectando del broker MQTT...")

#finally:
    #client.disconnect()
    #logging.info("Se ha desconectado del broker. Saliendo...")
