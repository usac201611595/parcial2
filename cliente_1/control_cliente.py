import threading
import time
from Cliente_pr12 import *

class Comnd(object):
    def __init__(self,topic,comando,user):#GAMS
        self.userid=userid#GAMS
        self.topic=topic#GAMS
        self.data = comando#GAMSs
    def hiloalive(self):
        cnt=0
        cnt2=0
        while True:
            #client.publish("comandos/12", C_ALIVE+b'$'+USERID, qos = 0, retain = False)#GAMS
            if self.ACK():
                cnt+=1
                if cnt=>3:
                    time.sleep(ALIVE_CONTINUOUS)
            else:
                cnt=0
                time.sleep(ALIVE_CONTINUOUS)

            print("enviando ALIVE")
            time.sleep(delay) #GAMSDelay en segundos

    def alive(self):
        t1 = threading.Thread( target = self.s_alive,
                                        daemon = True
                                        )
        t1.start()
    def ACK(self):#GAMS
        return self.data==binascii.unhexlify("05") and self.usuario==USERID and self.topic=="comandos/12"#GAMS
#    def FRR(self):#GAMS
#        return self.data==binascii.unhexlify("02") and self.topic=="comandos/12"+USERID.decode("utf-8")#GAMS
#    def Ok(self):
#        return self.data==binascii.unhexlify("06") and self.usuario==USERID and self.topic=="comandos/12"#GAMS
#    def No(self):#GAMS
#        return self.data==binascii.unhexlify("07") and self.usuario==USERID and self.topic=="comandos/12"#GAMS
#    def __str__(self):#GAMS
#        return str(self.comando)#GAMS
#    def __repr__(self):#GAMS
#        return self.__str__()#
