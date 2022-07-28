
#先于socket_p1.py运行

import socket
import sig_partwo as s2
import json
#msg=input("请输入Z,M\n")
#Z,M=msg.split(" ")
HOST="127.0.0.1"
PORT=5088
dst=("127.0.0.1",9000)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#绑定端口和端口号
s.bind((HOST,PORT))
print("当前监听地址：",(HOST,PORT))
n,G,d2,k2,k3=s2.init()
print("————————————————————————————初始化成功————————————————————————————")
print("n=",n,"\nG=",G,"\nd2=",d2,"\nk2=",k2,"\nk3=",k3)
temp=s.recv(1024)
P1=json.loads(temp.decode("utf-8"))
pk=s2.Gen_pk(d2,P1,G,n)
print("-"*20+"Public Key 生成成功"+"-"*20)
print("pk ",pk)
s.sendto(json.dumps(pk).encode("utf-8"),dst)
Q1e=s.recv(1024)
Q1,e=json.loads(Q1e.decode("utf-8"))
s.sendto(json.dumps(s2.Gen_r(d2,k2,k3,Q1,e,n,G)).encode("utf-8"),dst)


