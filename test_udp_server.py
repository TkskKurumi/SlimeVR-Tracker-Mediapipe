import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 6005))
print("UDP bound on port 6000...")
az=b'\x03Hey OVR =D 5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
cnt=30
while cnt:
    data, addr = s.recvfrom(1024)
    #print("Receive from %s:%s" % addr)
    if data == b"exit":
        s.sendto(b"Good bye!\n", addr)
        continue
    if data[3]==3:
        s.sendto(az,addr)
    if(data):
        cnt-=1
    print(data)
    s.sendto(b"Hello %s!\n" % data, addr)