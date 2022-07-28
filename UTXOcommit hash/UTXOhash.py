import hashlib
import os
import ECC
def str_hash_int(msg:str):
    hmsg=hashlib.sha256(msg.encode("utf-8")).hexdigest()
    return int(hmsg,16)
def Gen_msg_ECCP(msg):#求消息对应的椭圆曲线的点的坐标
    nonce = 0
    while True:
        t=str_hash_int(msg)
        temp =str(nonce)+str(t)
        #print(temp)
        x = str_hash_int(temp)
        y = ECC.get_y(x)  # 求出哈希值作为x，求出对应的y
        if y != None:
            #print(nonce)
            return (str(msg)+"  ||  "+str(nonce),x,y)
        nonce += 1
hashoutput=open("hashoutput","w+")
hash_ret=[-1,-1]#集合hash结果初始值为无穷远点
with open("UTXO.txt") as f:
    for line in f:
        m,h_num,y=Gen_msg_ECCP(line[:-1])
        hashoutput.write(m+"  ||  "+str(h_num)+" : "+str(y)+"\n")
        hash_ret=ECC.Point_Add(hash_ret,(h_num,y))

print("UTXO集合的hash值为：",hash_ret)#输出集合的hash值
hashoutput.close()