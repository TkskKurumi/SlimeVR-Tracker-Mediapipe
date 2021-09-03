import socket,struct,random
#to be translated from SlimeVR-Tracker-ESP/src/udpclient.cpp
from constants import *

last_port=6970
class client:
    port=6969
    def __init__(self,host='127.0.0.1',mac=None,port=None):
        if(port is None):
            global last_port
            port=last_port
            last_port+=1
        self.byteOrder='!'
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('127.0.0.1',port))
        self.buff=bytearray()
        self.target=(host,c_misc.target_port)
        if(mac is None):
            self.mac=[random.randrange(256) for i in range(6)]
        self.handling_receive=False
        self.send_handshake()
        
    def clear_buff(self):
        self.buff.clear()
    def send_heartbeat(self):
        self.send_type(c_packet_type.PACKET_HEARTBEAT)
        self.send_packet_number()
    def handle_receive(self):
        
        if(self.handling_receive):
            return
        self.handling_receive=True
        data,addr=self.socket.recvfrom(1024)
        le=len(data)
        if(le):
            incoming_type=data[0]
            if(incoming_type==c_packet_type.PACKET_RECIEVE_HEARTBEAT):
                self.send_heartbeat()
            elif(incoming_type==c_packet_type.PACKET_RECIEVE_VIBRATE):
                print('~~~Received VIBRATE!!!~~~')
            elif(incoming_type==c_packet_type.PACKET_RECIEVE_HANDSHAKE):
                print('received handshake')
            elif(incoming_type==c_packet_type.PACKET_RECIEVE_COMMAND):
                print('command',data)
            elif(incoming_type==c_packet_type.PACKET_CONFIG):
                print('config',data)
            elif(incoming_type==c_packet_type.PACKET_PING_PONG):
                self.buff.append(data)
                self.sb()
            
        self.handling_receive=False
    def send_buff(self):
        self.handle_receive()
        #print(self.buff,self.target)
        self.socket.sendto(self.buff,self.target)
        self.buff.clear()
    clear=clear_buff
    sb=send_buff
    def send_packet_number(self):
        self.buff.extend(c_packets.eight_zero)
        self.sb()
    def send_type(self,type):   #int type
        self.buff.extend([0,0,0])
        self.buf_int32(type)
        self.sb()
    def buf_float(self,f):
        self.buff.extend(struct.pack(self.byteOrder+'f',f))
    def buf_int64(self,q):
        self.buff.extend(struct.pack(self.byteOrder+'q',q))
    def buf_int32(self,i):
        self.buff.extend(struct.pack(self.byteOrder+'i',i))
    def buf_str(self,s):
        self.buff.extend(struct.pack(self.byteOrder+'s',s.encode('ascii')))
    #rot: tuple(x,y,z,w)
    #data_type: sensor.DATA_TYPE_NORMAL | sensor.DATA_TYPE_CORRECTION
    #accuracy: 0
    def send_rotation(self,rot,data_type=sensor.DATA_TYPE_NORMAL,type=c_packet_type.PACKET_ROTATION_DATA,accuracy=0,sensor_id=0):
        x,y,z,w=rot
        print(rot,type)
        self.send_type(type)
        self.send_packet_number()
        self.buff.append(sensor_id)
        self.buff.append(data_type)
        self.buf_float(x)
        self.buf_float(y)
        self.buf_float(z)
        self.buf_float(w)
        self.buff.append(accuracy)
        self.sb()
    def send_sensor_info(self,id=0,sensor_state=1,type=c_packet_type.PACKET_SENSOR_INFO):
        self.send_type(type)
        self.send_packet_number()
        self.buff.append(id)
        self.buff.append(sensor_state)
        self.sb()
    def send_handshake(self):
        print('send handshake')
        self.send_type(c_packet_type.PACKET_HANDSHAKE)
        self.send_packet_number()
        self.buf_int32(c_misc.BOARD_CUSTOM) 
        self.buf_int32(c_misc.IMU_BNO085)   #fake
        self.buf_int32(c_misc.HARDWARE_MCU) #1 for esp8266
        self.buf_int32(0)
        self.buf_int32(0)
        self.buf_int32(0)
        self.buf_int32(1)   #firmware build number
        self.buf_str("0.0.1")
        for i in self.mac:
            self.buff.append(i)
        self.sb()
        