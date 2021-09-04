import socket
import struct
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 6005))
print("UDP bound on port 6000...")
az=b'\x03Hey OVR =D 5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
cnt=5
while cnt:
    data, addr = s.recvfrom(1024)
    #print("Receive from %s:%s" % addr)
    if data == b"exit":
        s.sendto(b"Good bye!\n", addr)
        continue
    
    if(data):
        if data[3]==3:
            s.sendto(az,addr)
        if(data[3]==1):
            #data=b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00?\x00\x00\x00?\x00\x00\x00?\x00\x00\x00?\x00\x00\x00'
            
            packet_num=data[4:12]
            x=data[12:16]
            y=data[16:20]
            z=data[20:24]
            w=data[24:28]
            x=struct.unpack(">f",x)
            y=struct.unpack(">f",y)
            z=struct.unpack(">f",z)
            w=struct.unpack(">f",w)
            print(packet_num,len(data),x,y,z,w)
        cnt-=1
        print(int(data[3]),data,len(data))
    #s.sendto(b"Hello %s!\n" % data, addr)