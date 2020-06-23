
TOPICS_AUDIO= "audio/20/" #MGHP parte inicial del TOPIC donde se recibiran los audios
TOPICS_CHAT="USUARIO/12/"
#MGHP nombre del archivo que contiene a los usuarios
usuarios='usuarios.txt' # MGHP variable que representa el archivo donde se tienen guardado los usuarios
salas='salas.txt'



def llama_subscripciones(topicsss,contenidos): # MGHP funcion que se encarga de crear una lista para poder utilizar la informacion de los usuarios
    qos = 2
    datos=[]

    archivo = open(contenidos, 'r') #MGHP abrimos el archivo que contiene la informacion de usuarios o salas
    for linea in archivo:
        registro=linea.split(',')
        registro[-1]=registro[-1].split('\n')[0]
        datos.append(registro)
    archivo.close()

    #for i in datos:
        #logging.info(i[:])

    #MGHP dentro de esta misma funcion nos subscribimos a los usuarios para poder recibir informacion

    for j in range(len(registro)):
        client.subscribe((topicsss+str(registro[j]),qos))#MGHP subscripcion a cada unos de los usuarios que estan dentrso del archivo
        logging.info(topicsss+str(registro[j]))# MGHP mostramos a que topics estamos susbcritos de los clientes

logging.info("subscribiendo a topics: ")
logging.info("PARA AUDIO: ")
#llama a la funcion que extrae la informacion de los documentos que contienen las salas y usuarios
llama_subscripciones(TOPICS_AUDIO,usuarios) #MGHP se subscribe a rececpion de audios de usuarios
llama_subscripciones(TOPICS_AUDIO,salas) #MGHP se subcribe recepcion de audios en salas
logging.info("PARA CHAT: ")
llama_subscripciones(TOPICS_CHAT,usuarios)#MGHP se subscribe a recepcion de chats en usuarios
llama_subscripciones(TOPICS_CHAT,salas)#MGHP se subscribe a recepcion de chats en salas.

logging.info("subscripcion exitosa")
