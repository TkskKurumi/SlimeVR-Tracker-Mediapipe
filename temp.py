import UdpClient
client=UdpClient.client()
#client.buff.extend(b'\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\xb2\xb5(\xbe\x88\x86\xff')
#client.sb()
client.buff.extend(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00?\x80\x00\x00')
client.sb()
client.buff.extend(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00?\x80\x00\x00')
client.sb()
client.buff.extend(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00?\x80\x00\x00')
client.sb()
client.buff.extend(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00?\x80\x00\x00')
client.sb()
client.buff.extend(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00?\x80\x00\x00')
client.sb()
client.buff.extend(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00?\x80\x00\x00')
client.sb()
