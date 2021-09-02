import socket
#to be translated from SlimeVR-Tracker-ESP/src/udpclient.cpp
from constants import *

last_port=6970
class client:
    port=6969
    def __init__(self,host='127.0.0.1',port=None):
        if(port is None):
            global last_port
            port=last_port
            last_port+=1
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1',port))
        self.buff=bytearray()
        self.target=(host,c_misc.target_port)
    def clear_buff(self):
        self.buff.clear()
    def send_buff(self):
        self.socket.sendto(self.buff,self.target)
    clear=clear_buff
    sb=send_buff
    def send_packet_number(self):
        self.buff.extend(c_packets.eight_zero)
        self.sb()
    def send_type(self,type):   #int type
        self.buff.extend([0,0,0,type])
        self.sb()
    def send_rotation(self,rot,data_type,accuracy,sensor_id,type):
        pass
