import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 6005))
print("UDP bound on port 6000...")

while True:
    data, addr = s.recvfrom(1024)
    print("Receive from %s:%s" % addr)
    if data == b"exit":
        s.sendto(b"Good bye!\n", addr)
        continue
    print(data)
    s.sendto(b"Hello %s!\n" % data, addr)