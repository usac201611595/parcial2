from import Cliente_pr12 import *
class Datos(object):
    #Gilmar Arnoldo Mendez Socorec 201611595
    def __init__(self,topicRoot,comando,receptor,mensaje):#GAMS
        self.topicRoot=topicRoot
        self.comando=comando
        self.receptor=receptor
        self.mensaje=mensaje
    def Peticion(self):#GAMS
        if comando=binascii.unhexlify("03"):
            return 
    def __str__(self):#GAMS
        return str(self.comando)#GAMS
    def __repr__(self):#GAMS
        return self.__str__()#GAMS
