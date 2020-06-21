ALIVE_PERIOD = 2 #GAMS Período entre envío de tramas ALIVE
ALIVE_CONTINUOUS = 0.1 #gAMS Período entre envío de tramas ALIVE si no hay respuesta


C_FTR = b'\x03' # LARP 'indicador' que el CLIENTE desea TRANSFERIR un archivo de audio a otros clientes, lo recibe le SERVIDOR
C_ALIVE = b'\x04' # LARP 'indicador' de que el CLIENTE esta ACTIVO
C_FRR = b'\x02' # LARP 'indicador' del SERVIDOR para los CLIENTES a quines les llegara el archivo de audio.
C_ACK = b'\x05' # LARP 'indicador' a) cuando el SERVIDOR recibe ALIVE, b) se TERMINA de RECIBIR un ARCHIVO
C_OK = b'\x06' # LARP 'indicador' de que el CLIENTE puede enviar el archivo puesto que CUMPLE el remitente y el destinatario $ el que ENVIA lo tomara como valido si esta su user-ID 201612268
C_NO = b'\x07' # LARP 'indicador' de NEGACION, a) si el REMITENTE o DESTINO no sena VALIDOS, el remitente SOLO lo tomara VALIDO si tiene su USER-ID

#System filenames
USERID= b'201611595'#GAMS
