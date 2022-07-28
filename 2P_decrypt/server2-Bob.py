import socket
import json
from SM2__ import *
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
#使用IPV4协议，使用UDP协议传输数据 B
#服务端主机IP地址和端口号，空字符串表示本机任何可用IP地址
HOST=""
PORT=5087
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#绑定端口和端口号
s.bind((HOST,PORT))
print('目前监听的端口号是：',PORT)
print("可以发送消息")
while True:
    
    sm2_B = SM2(ID='Bob')
    print("我是Bob,由我来协助Alice进行解密\n")
    #收到T1
    data0,addr=s.recvfrom(1024)
    #print("T1[0]:",data0.decode("utf8","ignore"))
    c=("T10接收成功")
    s.sendto(c.encode(),addr)
    
    data1,addr=s.recvfrom(1024)
    #print("T1[1]:",data1.decode())
    
    c=("T11接收成功")
    s.sendto(c.encode(),addr)
    T1=(int(data0.decode()),int(data1.decode()))
    print("接收到的T1为：",T1)
    T2=sm2_B.multiply(get_inverse(sm2_B.sk,sm2_B.n),T1)
    print("发送过去的T2为：",T2)
        #将T2发送过去
    T2=list(T2)
    s.sendto(str(T2[0]).encode(),addr)
    data,addr=s.recvfrom(1024)
    print(data.decode())
    
    s.sendto(str(T2[1]).encode(),addr)
    data,addr=s.recvfrom(1024)
    print(data.decode())
    break

    
s.close()
