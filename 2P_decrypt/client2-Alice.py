import socket
import json
from SM2__ import *
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # 创建 socket 对象
while True:
    sm2_A = SM2(ID='Alice')
    print("我是Alice，收到密文后，在Bob的帮助下我将进行解密\n")
    sm2_B = SM2(ID='Bob')
    dA=sm2_A.sk
    dB=sm2_A.sk
    P=sm2_A.multiply(get_inverse(dA*dB-1,sm2_A.n),sm2_A.G)
    M = "需要解密"
    k = 0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F
    print("加密的信息为：",M)
    res, C = sm2_A.encrypt(M, P, k)
    if not res:
        print('A报告加密错误：', C)
    #print(type(C))
    print("生成的密钥密文为：",C.hex())
   
    x1 = to_int(C[:sm2_A.keysize])
    y1 = to_int(C[sm2_A.keysize:sm2_A.keysize << 1])
    C1 = (x1, y1)
    if sm2_A.is_zero(C1):  # S
       break
    T1 = sm2_A.multiply(get_inverse(sm2_A.sk,sm2_A.n), C1)
    
    print("发送过去的T1为：",T1)
    T1=list(T1)
    s.sendto(str(T1[0]).encode(),("192.168.1.5",5088))
    data,addr=s.recvfrom(1024)
    print(data.decode())
    
    s.sendto(str(T1[1]).encode(),("192.168.1.5",5088))
    data,addr=s.recvfrom(1024)
    print(data.decode())
    #print(
    
    #收到T2
    data0,addr=s.recvfrom(1024)
    c=("T20接收成功")
    s.sendto(c.encode(),("192.168.1.5",5088))
    
    data1,addr=s.recvfrom(1024)
    #print("T2[1]:",data1.decode())
    c=("T21接收成功")
    s.sendto(c.encode(),("192.168.1.5",5088))
    
    T2=(int(data0.decode()),int(data1.decode()))
    print("接收的T2为：",T2)
    x2,y2=sm2_A.add(T2,sm2_A.minus(C1))
    klen = len(C) - (sm2_A.keysize << 1) - HASH_SIZE << 3
    t=to_int(KDF(join_bytes([x2, y2]), klen))
    C2 = C[sm2_A.keysize << 1:-HASH_SIZE]
    M = to_byte(to_int(C2) ^ t, klen >> 3)
    u = sm3(join_bytes([x2, M, y2]))
    C3 = C[-HASH_SIZE:]
    if u != C3:
        #print("解密得到：需要解密")
        print("解密失败")
        break
    print("解密得到：",M)
    break


s.close()
