import socket
import sig_partone as s1
import json
import ECC
import hashlib
def sig_verify(M,sig,pk,n,G):
    r,s=sig
    e =int(hashlib.sha256(M.encode('utf-8')).hexdigest(),16)
    #print(hex(e))
    t=(r+s)%n
    x,y=ECC.Point_Add(ECC.Multi(s,G),ECC.Multi(t,pk))
    R=(e+x)%n
    if R==r:
        return True
    else:
        return False

msg=input("请输入Z,M （用空格分开）\n")
Z,M=msg.split(" ")
print(Z+M)
HOST="127.0.0.1"
PORT=9000
dst=("127.0.0.1",5088)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#绑定端口和端口号
s.bind((HOST,PORT))
print("当前监听地址：",(HOST,PORT))
n,G,d1,k1=s1.init()
print("————————————————————————————初始化成功————————————————————————————")
print("n=",n,"\nG=",G,"\nd1=",d1,"\nk1=",k1)
P1=s1.geneP1(d1,G,n)
s.sendto(json.dumps(P1).encode("utf-8"),dst)
print("-"*25+"-"*20)
print("发送P1成功：P1=",P1)
pk=json.loads(s.recv(1024).decode("utf-8"))
print("-"*25+"-"*20)
print("收到Public key :",pk)
Q1e=s1.genQe(Z,M,k1,G)
s.sendto(json.dumps(Q1e).encode("utf-8"),dst)
print("-"*25+"-"*20)
print("Q1,e发送成功 (Q1,e)=",Q1e)
r,s2,s3=json.loads(s.recv(1024).decode("utf-8"))
print("-"*25+"-"*20)
print("success recieve (r,s2,s3):",(r,s2,s3))
r,s=s1.Gen_sig(r,s2,s3,d1,k1,n)
print("-"*20+"签名生成成功"+"-"*20)
print((r,s))

print("-"*20+"开始验证签名"+"-"*20)
print("签名验证结果为")
print(sig_verify(Z+M,(r,s),pk,n,G))