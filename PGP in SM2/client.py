import socket  # 导入 socket 模块 A
import json
from SM2 import *
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # 创建 socket 对象
while True:
     # A、B双方初始化
    sm2_A = SM2(ID='Alice')
    sm2_B = SM2(ID='Bob')
    # A、B均掌握对方的公钥和ID
    PB, IDB = sm2_B.pk, sm2_B.ID
    print("---------------------------密钥协商阶段-Alice---------------------------")
    # A 发起协商
    rA, RA = sm2_A.agreement_initiate()
    # A将RA发送给B
    print("发送的RA;",RA)
    data=json.dumps(list(RA))
    s.sendto(data.encode(),("192.168.1.5",5088))
    print("RA发送完毕")
    
    # A 协商确认
    data0,addr=s.recvfrom(1024)
  
    
    data1,addr=s.recvfrom(1024)
    
    RB=(int(data0.decode()),int(data1.decode()))
    
    SB,addr=s.recvfrom(1024)
    print("收到的SB:",SB)
    print("SB接收完毕")
   
    KA=0
    res, content ,KA= sm2_A.agreement_confirm(rA, RA, RB, PB, IDB, SB,KA,option=True)
    
    #if not res:
        #print('A报告协商错误：', content)
        #break
    #KA,SA = content
   # print("content:",content)
    #print("SA:",SA)

    
    # A将(选项SA)发送给B
    #c=SA
    #print("发送的SA:",SA)
    #s.sendto(c.encode(),("192.168.1.5",5088))
    #print("SA发送完毕")
    #print('KA == KB?: %s, value: 0x%s, len: %d' % (KA == KB, KA.hex(), len(KA) << 3))
   
    #data=str(KA).encode()
    s.sendto(KA,("192.168.1.5",5088))
    #break
    #A向B发送数据B进行解密
    #KA KA用于对称密码加解密用来发送消息
    print("协商的密钥为：",KA.hex())
    print("---------------------------协商密钥完毕---------------------------")
    
    print("---------------------------AES加密消息阶段（用协商密钥）------------------------")
    message = "需要加密的信息"
    key = KA
    mode = AES.MODE_OFB
    cryptor = AES.new(key, mode, b'0000000000000000')
    length = 16
    count = len(message)
    if count % length != 0:
        add = length - (count % length)
    else:
        add = 0
    message = message + ('\0' * add)
    ciphertext = cryptor.encrypt(message.encode('utf-8'))
    result = b2a_hex(ciphertext)
    print(result.decode('utf-8'))

   
    s.sendto(result,("192.168.1.5",5088))
    print("发送消息密文完毕")
    print("---------------------------加密消息完毕---------------------------")
     
    print("---------------------------加密密钥阶段（用Bob公钥）---------------------------")
    #公私钥用来对对称密码的密钥进行加密,B的公钥加密
    M = KA
    k = 0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F
    print("加密的密钥为：",M.hex())
    # A用B的公钥对消息M进行加密
    res, C = sm2_A.encrypt(M, PB, k)
    if not res:
        print('A报告加密错误：', C)
    print("发送的密钥密文为：",C)
    s.sendto(C,("192.168.1.5",5088))
    print("发送密钥密文完毕")
    print("---------------------------加密密钥完毕---------------------------")
    
    break
    
s.close()
