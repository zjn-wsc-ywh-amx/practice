import socket
import json
from SM2 import *
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
#使用IPV4协议，使用UDP协议传输数据 B
#服务端主机IP地址和端口号，空字符串表示本机任何可用IP地址
HOST=""
PORT=5088
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#绑定端口和端口号
s.bind((HOST,PORT))
print('目前监听的端口号是：',PORT)
print("可以互相发送消息")
while True:
    print("---------------------------密钥协商阶段-Bob---------------------------")
    sm2_A = SM2(ID='Alice')
    sm2_B = SM2(ID='Bob')
    PA,IDA = sm2_A.pk, sm2_A.ID
    dB=sm2_B.sk
    # B 响应协商
    data,addr=s.recvfrom(1024)
    RA=json.loads(data)
    RA=(RA[0],RA[1])
    print("收到的RA:",RA)
    print("RA接收完毕")
    res, content = sm2_B.agreement_response(RA, PA, IDA,option=True)
    if not res:
        print('B报告协商错误：', content)
        break
    RB, KB, SB, S2 = content
    print("发送的RB:",RB)
    print("发送的SB:",SB)
      # B将RB、(选项SB)发送给A
    #发送RB

    RB=list(RB)
    s.sendto(str(RB[0]).encode(),addr)
    s.sendto(str(RB[1]).encode(),addr)
    print("RB发送完毕")
    #发送SB
    s.sendto(SB,addr)
    print("SB发送完毕")
    
     # B 协商确认,收到SA
    data,addr=s.recvfrom(1024)
    KB=data
    
    print("协商的密钥为：",KB.hex())
    print("---------------------------协商密钥完毕---------------------------")
    #data,addr=s.recvfrom(1024)
    #SA=data.decode()
   # print("SA:",SA)
    #res, content = sm2_B.agreement_confirm2(S2, SA)
    #if not res:
       # print('B报告协商错误：', content)
        #break
    #结束监听
       
    print("---------------------------AES消息解密阶段（用协商密钥）------------------------")
    data,addr=s.recvfrom(1024)
    print("收到的密文：",data.decode())
    result=data.decode()
    key=KB
    mode = AES.MODE_OFB
    cryptor = AES.new(key, mode, b'0000000000000000')
    plain_text = cryptor.decrypt(a2b_hex(result))
    print("解密的信息为：")
    print(plain_text.decode('utf-8').rstrip('\0'))
    print("---------------------------解密消息完毕---------------------------")
    
    #解密密钥
    print("---------------------------解密密钥阶段（用Bob私钥）---------------------------")
    data,addr=s.recvfrom(1024)
    print("收到的密钥密文为：",data)
    C=data
    print(type(C))
    res, M2 = sm2_B.decrypt(C)
    if not res:
        print('B报告解密错误：', M2)
        break
    print('解密的密钥为：',key.hex())
    print("---------------------------解密密钥完毕---------------------------")
    break
       
s.close()
